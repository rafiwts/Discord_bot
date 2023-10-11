import discord
from discord.ext import commands

from ai_chatgpt.chat_bot import discord_chat_gpt

from .parsing_handlers import (
    get_city_temperature,
    get_encouragement_quote,
    get_store_products,
)
from .validators import ValidationView as validation
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
            return message.channel.send(events.return_all_events())

        if message.content.strip() == "showcommands":
            return message.channel.send(commands.return_all_commands())

    @classmethod
    def return_on_event(cls, message: discord.Message):
        if message.content.strip().startswith(dict_of_events["chatgpt"]):
            users_input = message.content.replace(dict_of_events["chatgpt"], "")
            chat_response = discord_chat_gpt(users_input)
            return message.channel.send(chat_response)
        elif message.content.strip() == dict_of_events["encourage"]:
            encouragement_quote = get_encouragement_quote()
            return message.channel.send(encouragement_quote)
        elif message.content.strip().startswith(dict_of_events["weather"]):
            user_response = message.content.split(",")
            try:
                # get country name from response
                list_of_strings = user_response[0].split(" ")[1:]
                country = " ".join(list_of_strings)
                city = user_response[1]

                temperature = get_city_temperature(country, city)

                return message.channel.send(temperature)
            except IndexError:
                return message.channel.send(validation.weather_value_validation())
        elif message.content.strip().startswith(dict_of_events["find_product"]):
            try:
                user_response = message.content.split()
                name = user_response[1]
                get_category_products = get_store_products(name=name)
                return message.channel.send(get_category_products)
            except IndexError:
                return message.channel.send(validation.no_product_valdation())
        elif message.content.strip().startswith(dict_of_events["find_category"]):
            try:
                user_response = message.content.split()
                category = user_response[1]
                get_category_products = get_store_products(category=category)
                return message.channel.send(get_category_products)
            except IndexError:
                return message.channel.send(validation.no_category_valdation())
        elif message.content.strip().startswith(dict_of_events["find_categories"]):
            get_category = get_store_products()
            return message.channel.send(get_category)
        elif message.content.strip().startswith(dict_of_events["find_products"]):
            try:
                user_response = message.content.split()
                # if user provided some value except @findproducts, validate it
                limit = int(user_response[1])
                if limit in range(1, 11):
                    get_products = get_store_products(limit=limit)
                    return message.channel.send(get_products)
                else:
                    return message.channel.send(validation.limit_range_validation())
            except (ValueError, IndexError):
                return message.channel.send(validation.limit_value_validation())

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
