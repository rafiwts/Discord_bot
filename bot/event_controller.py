import discord

from database.models import DiscordUser, Command, Message
#TODO: finish the connection to the database 
class Controller:
    async def message_controller(self, message: discord.Message) -> None:
        user = message.author
        print(user)
        print('--------')
        print(message)

    async def reaction_controller(self, reaction: discord.RawReactionActionEvent) -> None:
        print(reaction)
    
    async def command_controller(self, message: discord.Message) -> None:
        author = message.author
        #TODO: add this to a different place - create a user in a database upon joining the guild? think about it
        # create a user if does not exist
        try:
            discord_user = DiscordUser.get(DiscordUser.username==message.author)
        except DiscordUser.DoesNotExist:
            discord_user = DiscordUser.create(
                username=author,
                guildname=author.guild,
                created_at=author.created_at,
                joined_at=author.joined_at,
                is_bot=author.bot)
            
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

