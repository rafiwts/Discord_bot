import discord
from database.models import Command, DiscordUser
#TODO: finish the connection to the database 
class Controller:
    async def message_controller(self, message: discord.Message) -> None:
        #FIXME: messages are also intercepted by command_controller
        user = message.author
        print(user)
        print('--------')
        print(message)

    async def reaction_controller(self, reaction: discord.RawReactionActionEvent) -> None:
        print(reaction)
    
    async def command_controller(self, message: discord.Message) -> None:
        author = message.author
        try:
            discord_user = DiscordUser.get(
                DiscordUser.username==message.author)
        except DiscordUser.DoesNotExist:
            discord_user = DiscordUser.create(
                username=author,
                guildname=author.guild,
                created_at=author.created_at,
                joined_at=author.joined_at,
                is_bot=author.bot)
            
            discord_user.save()
            
        command = Command.get_or_none(
            (Command.content==message.content) &
            (Command.user==discord_user.id)
        )

        if command is None:
            command = Command.create(
                content=message.content,
                created=message.created_at,
                user=discord_user.id
            )
            command.save()
        #TODO: change the columns -> first_created/last_updated/number_of_calls if exists
        #TODO: maybe add a user to a database upon joining add add an aditional method on_joining?
            
        print(message.content)

