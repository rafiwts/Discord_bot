import discord


class Controller:
    async def message_controller(self, message: discord.Message) -> None:
        print(message)

    async def reaction_controller(self, reaction: discord.RawReactionActionEvent) -> None:
        print(reaction)
    
    async def command_controller(self, message: discord.Message) -> None:
        print(message)
