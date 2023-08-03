import discord
from discord.ext import commands
import peewee

from database.models import DiscordUser, Command, Message, BotUser, Reaction

#TODO: finish the connection to the database 
class Controller:
    #why does it need a second parameter - controller in 3 methods?
    async def message_create_controller(controller,
                                        sent_message: discord.Message) -> None:
        discord_user = DiscordUser.get_or_none(username=sent_message.author)
        if discord_user is None:
            discord_user = DiscordUser.create_new_user(username=sent_message.author,
                                                       guildname=sent_message.author.guild,
                                                       created_at=sent_message.author.created_at,
                                                       joined_at=sent_message.author.joined_at)
            
            discord_user.save()
        
        new_message = Message.create_new_message(message_id=sent_message.id,
                                                 content=sent_message.content,
                                                 first_created=sent_message.created_at,
                                                 user=discord_user.id)

        new_message.save() 

    async def message_edit_cotroller(controller,
                                     sent_message: discord.Message,
                                     edited_message: discord.Message):

        Message.edit_message(message_id=sent_message.id,
                             new_content=edited_message.content,
                             edited_at=edited_message.edited_at)
    
    async def message_delete_controller(controller,
                                        sent_message: discord.Message):
        try:
            existing_message = Message.get_by_id(sent_message.id)
            existing_message.delete_instance()
        except Message.DoesNotExist:
            return

    async def reaction_controller(self, reaction: discord.RawReactionActionEvent) -> None:
        print(reaction.event_type)
        if reaction.event_type == 'REACTION_ADD':
            reaction_to_message = Reaction.create_new_reaction(user_from=reaction.user_id,
                                                               user_to=reaction.member.id,
                                                               message=reaction.message_id)
            
            reaction_to_message.save()
        else:
            reaction_to_message = Reaction.get(user_from=reaction.user_id,
                                           user_to=reaction.member.id,
                                           message=reaction.message_id)
            
            reaction_to_message.delete_instance()

    async def command_controller(self, message: discord.Message) -> None:
        #TODO: if no command exist, it throws an error
        user = message.author
        existing_discord_user, new_discord_admin = DiscordUser.get_or_create(
            username=user,
            defaults={'guildname': user.guild,
                      'created_at': user.created_at,
                      'joined_at': user.joined_at})
        
        if existing_discord_user is None:
            new_discord_admin.save()
            new_discord_admin = existing_discord_user
        
        new_command = Command.get_or_none((Command.content==message.content) &
                                          (Command.user==existing_discord_user.id))

        if new_command is None:
            new_command = Command.create_new_command(content=message.content,
                                                     first_created=message.created_at,
                                                     user=existing_discord_user.id)
            
            new_command.save()
        else:
            update_counter = Command.increment_counter(last_updated=message.created_at,
                                                       command_counter=Command.command_counter + 1,
                                                       message=message.content,
                                                       discord_user=existing_discord_user.id)
            
            update_counter.execute()
        #if it is a commands, is is saved in command and message table separately
        new_message = Message.create_new_message(message_id=message.id,
                                                 content=message.content,
                                                 first_created=message.created_at,
                                                 user=existing_discord_user.id,
                                                 command=new_command.id)
        
        new_message.save()
      
        #TODO: commands are also messages - we want to save all messages created by the user - commands are only part of it
        #TODO: think about the events and event model 
        print(message.content)

    async def bot_controller(self, bot: commands.Bot, guild: str) -> None:
        #the user who owns a bot is an admin at the same time
        #TODO: how to fetch the joined_at parameter 
        admin_user = DiscordUser.get_or_none(username=bot.application.owner.name)
        if admin_user is None:
            new_admin_user = DiscordUser.create_new_admin(username=bot.application.owner.name,
                                                          guildname=guild,
                                                          created_at=bot.application.owner.created_at)
            
            new_admin_user.save()
        else:
            new_admin_user = DiscordUser.update_user_to_admin(bot.application.owner.name)
          
        try:
            new_discord_bot = BotUser.create_new_bot(botname=bot.user,
                                                     command_prefix=bot.command_prefix,
                                                     owner_id=new_admin_user.id)
            new_discord_bot.save()
        except peewee.IntegrityError:
            return
       


        # try:
        #     new_bot_owner = DiscordUser.get(DiscordUser.username==bot.application.owner.name)
        #     new_bot_owner.is_admin = True
        #     new_bot_owner.save()
        # except DiscordUser.DoesNotExist:
        #     new_bot_owner = DiscordUser.create_new_user(username=bot.application.owner.name,
        #                                                        guildname=guild,
        #                                                        created_at=bot.application.owner.created_at,
        #                                                        joined_at=bot.application.owner.joined_at,
        #                                                        is_admin=True)
            
        #     new_bot_owner.save()
            
        print(bot.command_prefix, bot.user, bot.status, list(bot.commands), bot.activity, bot.application_id,
              bot.owner_id, bot.application, bot.help_command)
        
        print(bot.application.name)
        print(bot.application.owner.name)

    async def user_controller(self, user: discord.Member, guild: str) -> None:
        #TODO: change - get or create
        existing_discord_user = DiscordUser.get_or_none(DiscordUser.username==user.name)
        if existing_discord_user is None:
            new_discord_user = DiscordUser.create_new_user(username=user.name,
                                                            guildname=guild,
                                                            created_at=user.created_at,
                                                            joined_at=user.joined_at)
            
            new_discord_user.save()
        else:
            existing_discord_user.delete_instance()
        