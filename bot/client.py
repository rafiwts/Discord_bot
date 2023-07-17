import discord
from discord.ext import commands

from .event_controller import Controller
from typing import Coroutine

class DiscordBot(commands.Bot):
    controller: Controller

    def initialize(self) -> None:
        self.controller = Controller()

    async def process_message(self, message: discord.Message) -> Coroutine:
        await self.controller.message_controller(message)

    async def process_reaction(self, reaction: discord.RawReactionActionEvent) -> Coroutine:
        await self.controller.reaction_controller(reaction)

    async def process_commands(self, message: discord.Message) -> Coroutine:
        await self.controller.command_controller(message)
        return await super().process_commands(message)