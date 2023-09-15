import discord
from discord.ext import commands

from .parsing_handlers import get_city_temperature, get_encouragement_quote
from .validators import ExceptionView as exception
from .view_lists import CommandsView, EventsView, dict_of_events


class ServerEvents:
    @classmethod
    def return_on_ready(cls, bot: commands.Bot, guild: discord.Guild, channel_id: int):
        channel = bot.get_channel(channel_id)
        return channel.send(
            f"""Hi Everyone! {bot.user} has just connected to {guild}
Below you will find a list of commands that you can use:
showevents: returns a list of actions
showcommands: returns a list of commands"""
        )

    @classmethod
    def return_on_message(
        cls,
        message: discord.Message,
        commands: CommandsView = CommandsView,
        events: EventsView = EventsView,
    ):
        if message.content.strip() == "showevents":
            # TODO: after finishing complete the list
            return message.channel.send(events.return_all_events())

        if message.content.strip() == "showcommands":
            return message.channel.send(commands.return_all_commands())

    @classmethod
    def return_on_event(cls, message: discord.Message):
        # TODO: implement the functionality
        if message.content.strip() == dict_of_events["askbot"]:
            pass
        elif message.content.strip() == dict_of_events["encourage"]:
            return message.channel.send(get_encouragement_quote())
        elif message.content.strip().startswith(dict_of_events["weather"]):
            users_response = message.content.split()
            try:
                country = users_response[1]
                city = users_response[2]

                temperature = get_city_temperature(country, city)

                return message.channel.send(temperature)
            except IndexError:
                return message.channel.send(exception.weather_value_exceptions())
        elif message.content.strip().startswith(dict_of_events["find_item"]):
            pass

    @classmethod
    def return_on_editing(
        cls,
        sent_message: discord.Message,
        edited_message: discord.Message,
        user: discord.Member,
    ):
        return edited_message.channel.send(f"{user} has edited the message")

    @classmethod
    def return_on_deleting(cls, message: discord.Message):
        return message.channel.send(f"{message.author} has deleted the message")

    @classmethod
    def return_on_typing(cls, channel: discord.TextChannel, user: discord.Member):
        return channel.send(
            f'Hi {user}! How can I help you? For more information, type "!info" command'
        )

    @classmethod
    def return_on_joining(cls, member: discord.Message, channel: discord.TextChannel):
        return channel.send(f"a new user {member} has entered the chat")

    @classmethod
    def return_on_removing(cls, member: discord.Member, channel: discord.TextChannel):
        return channel.send(f"{member} has been removed")

    @classmethod
    def return_on_updating(cls, old_user: discord.Member, channel: discord.TextChannel):
        return channel.send(f"{old_user} has updated their profile")

    @classmethod
    def return_on_banning(
        cls, guild: discord.Guild, member: discord.Member, channel: discord.TextChannel
    ):
        return channel.send(f"{member} has been temporarily banned from {guild}")

    @classmethod
    def return_on_unbanning(
        cls, guild: discord.Guild, member: discord.Member, channel: discord.TextChannel
    ):
        return channel.send(f"{member} has been unbanned from {guild}")
