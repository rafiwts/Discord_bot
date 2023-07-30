import discord
from discord.ext import commands

from .event_controller import Controller
from typing import Coroutine

class DiscordBot(commands.Bot):
    #TODO: add additional methods after dealing with databases and relations between columns
    controller: Controller

    def initialize(self) -> None:
        self.controller = Controller()

    async def process_message(self, old_message: discord.Message, 
                                    new_message: discord.Message = None) -> Coroutine:
        await self.controller.message_controller(old_message, new_message)

    async def process_reaction(self, reaction: discord.RawReactionActionEvent) -> Coroutine:
        await self.controller.reaction_controller(reaction)

    async def process_commands(self, message: discord.Message) -> Coroutine:
        await self.controller.command_controller(message)
        return await super().process_commands(message)
    
    async def process_bot(self, bot: commands.Bot, guild: str) -> Coroutine:
        await self.controller.bot_controller(bot, guild)

    async def process_user(self, member: discord.Member, guild: str) -> Coroutine:
        await self.controller.user_controller(member, guild)