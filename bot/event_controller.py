import discord
from discord.ext import commands

from database.models import DiscordUser, Command, Message, BotUser

#TODO: finish the connection to the database 
class Controller:
    async def message_controller(self, message: discord.Message) -> None:
        user = message.author
        

    async def reaction_controller(self, reaction: discord.RawReactionActionEvent) -> None:
        print(reaction)
    
    async def command_controller(self, message: discord.Message) -> None:
        user = message.author
        #TODO: add this to a different place - create a user in a database upon joining the guild? think about it
        # create a user if does not exist
        try:
            discord_user = DiscordUser.get(DiscordUser.username==message.author)
        except DiscordUser.DoesNotExist:
            discord_user = DiscordUser.create(
                username=user,
                guildname=user.guild,
                created_at=user.created_at,
                joined_at=user.joined_at,
                is_bot=user.bot)
            
            discord_user.save()
        #save a message to the database
     
        #add a new command for a given user or increment the counter if already exists  
        new_command = Command.get_or_none(
            (Command.content==message.content) &
            (Command.user==discord_user.id))

        if new_command is None:
            new_command = Command.create(content=message.content,
                                         first_created=message.created_at,
                                         user=discord_user.id)
            
            new_command.save()
        else:
            update_command = Command.update(last_updated=message.created_at,
                                            command_counter=Command.command_counter + 1)\
                            .where((Command.content==message.content) &
                                   (Command.user==discord_user.id))

            update_command.execute()

        new_message = Message.create(content=message.content,
                                     created_at=message.created_at,
                                     user=discord_user.id,
                                     command=new_command.id)
        
        new_message.save()
        #TODO: change a column message - add a number of reactions --> maybe add a table reaction
        #TODO: maybe add a user to a database upon joining add add an aditional method on_joining?
        #TODO: commands are also messages - we want to save all messages created by the user - commands are only part of it
        #TODO: think about the events and event model 
        print(message.content)

    async def bot_controller(self, bot: commands.Bot, guild: int) -> None:
        try:
            bot_owner = DiscordUser.get(DiscordUser.username=='rafiwts')
        except DiscordUser.DoesNotExist:
            bot_owner = DiscordUser.create(username=bot.application.owner.name,
                                           guildname=guild)
            
            bot_owner.save()
    
        new_bot = BotUser.get_or_none(BotUser.botname==bot.user)
        if new_bot is None:
            new_bot = BotUser.create(botname=bot.user,
                                     command_prefix=bot.command_prefix,
                                     owner_id=bot_owner.id)
            
            new_bot.save()

            
        print(bot.command_prefix, bot.user, bot.status, list(bot.commands), bot.activity, bot.application_id,
              bot.owner_id, bot.application, bot.help_command)

    async def user_controller(self, user: discord.Member) -> None:
        pass