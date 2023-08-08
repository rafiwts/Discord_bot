import discord
from discord.ext import commands
from datetime import datetime
import peewee

from database.models import DiscordUser, Command, Message, BotUser, Reaction, Event

class Controller:
    #FIXME: why does it need a second parameter - controller in 3 methods?
    async def message_create_controller(self, sent_message: discord.Message) -> None:
        sender = sent_message.author
        discord_user = DiscordUser.get_or_create_user(sender)
        
        new_message = Message.create_new_message(sent_message=sent_message,
                                                 user=discord_user.id)

        new_message.save() 

    async def message_edit_cotroller(self, sent_message: discord.Message,
                                           edited_message: discord.Message):

        Message.edit_message(discord_id=sent_message.id,
                             edited_message=edited_message)
    
    async def message_delete_controller(self, sent_message: discord.Message):
        try:
            existing_message = Message.get(discord_id=sent_message.id)
            existing_message.delete_instance()
        except Message.DoesNotExist:
            return
        
    async def event_controller(self, sent_message: discord.Message):
        sender = sent_message.author
        discord_user = DiscordUser.get_or_create_user(sender)
        current_event = Event.get_or_none(name=sent_message.content,
                                          user=discord_user.id)
        if current_event is None:
            new_event = Event.create_new_event(user=discord_user.id,
                                               sent_message=sent_message)
        
            new_event.save() 
        else:
            update_event = Event.increment_counter(user=discord_user.id,
                                                   sent_message=sent_message,
                                                   counter=Event.counter + 1)
            
            update_event.execute()

    async def reaction_controller(self, reaction: discord.RawReactionActionEvent) -> None:
        #FIXME: counter - delete it? cause one user can have multiple reactions
        current_message = Message.get_or_none(discord_id=reaction.message_id)
        if current_message is None:
            # do not save reactions from bot's messages
            return
        user = BotUser.check_user_or_bot(discord_id=reaction.user_id)
       
        if reaction.event_type == 'REACTION_ADD':
            reaction_for_existing_message = Reaction.get_or_none(user_from=user.id,
                                                                 user_to=current_message.user.id,
                                                                 message=current_message.id)
            if reaction_for_existing_message is None: 
                reaction_to_message = Reaction.create_new_reaction(user_from=user.id,
                                                                   current_message=current_message)
         
                reaction_to_message.save()
                     
                Message.edit_message(discord_id=reaction.message_id,
                                     reaction_counter=Message.reaction_counter + 1)
            else:    
                Reaction.update(edited_at=datetime.now())\
                        .where((Reaction.user_to==current_message.user.id) & 
                               (Reaction.message==current_message.id))\
                        .execute()
        else: 
            reaction_to_message = Reaction.get(user_from=user.id,
                                               user_to=current_message.user.id,
                                               message=current_message.id)
        
            reaction_to_message.delete_instance()

            Message.edit_message(discord_id=reaction.message_id,
                                 reaction_counter=Message.reaction_counter - 1)
                
    async def command_controller(self, message: discord.Message) -> None:
        #TODO: if no command exist, it throws an error
        sender = message.author
        discord_user = DiscordUser.get_or_create_user(sender)
        
        new_command = Command.get_or_none((Command.content==message.content) &
                                          (Command.user==discord_user.id))

        if new_command is None:
            new_command = Command.create_new_command(message=message,
                                                     user=discord_user.id)
            
            new_command.save()
        else:
            update_counter = Command.increment_counter(command_counter=Command.command_counter + 1,
                                                       message=message,
                                                       discord_user=discord_user.id)
            
            update_counter.execute()
        #if it is a commands, is is saved in command and message table separately
        new_message = Message.create_new_message(sent_message=message,
                                                 user=discord_user.id,
                                                 command=new_command.id)
        
        new_message.save()

    async def bot_controller(self, bot: commands.Bot, guild: str) -> None:
        #TODO: how to fetch the joined_at parameter 
        admin_user = DiscordUser.get_or_none(discord_id=bot.application.owner.id)
        if admin_user is None:
            new_admin_user = DiscordUser.create_new_admin(bot_owner=bot.application.owner,
                                                          guildname=guild)
                                                      
            new_admin_user.save()
        else:
            new_admin_user = DiscordUser.update_user_to_admin(bot.application.owner.id)
          
        try:
            new_discord_bot = BotUser.create_new_bot(bot=bot,
                                                     owner_id=new_admin_user.id)
            new_discord_bot.save()
        except peewee.IntegrityError:
            return

    async def user_controller(self, user: discord.Member, guild: str) -> None:
        existing_discord_user = DiscordUser.get_or_none(DiscordUser.discord_id==user.id)
        if existing_discord_user is None:
            new_discord_user = DiscordUser.create_new_user(discord_user=user,
                                                           guildname=guild)
            
            new_discord_user.save()
        else:
            existing_discord_user.delete_instance()
        