import discord

from .view_lists import dict_of_events


class ExceptionView:
    @staticmethod
    def weather_value_exception():
        description = (
            "Something went wrong! Check if the data "
            "you have typed are correct and in correct order"
        )

        return description

    @staticmethod
    def response_to_discord_exception(message: discord.Message):
        user_input = message.content.replace(dict_of_events["chatgpt"], "")
        description = (
            f"The response for your question - a ChatGPT request "
            f'"{user_input.strip()}" is too long to be processed by discord. '
            "Please visit https://chat.openai.com for details"
        )

        return message.channel.send(description)
