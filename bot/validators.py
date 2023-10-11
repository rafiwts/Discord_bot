import discord

from .view_lists import dict_of_events


class ValidationView:
    @staticmethod
    def weather_value_validation():
        description = (
            "Something went wrong! Check if the data "
            "you have typed are correct and in correct order"
        )

        return description

    @staticmethod
    def response_to_discord_validation(message: discord.Message):
        # FIXME: how to return many messages if the response is too long?
        # can I split it ?
        user_input = message.content.replace(dict_of_events["chatgpt"], "")

        if user_input.strip() == "@chatgpt":
            description = (
                f"The response for your question - a ChatGPT request "
                f'"{user_input.strip()}" is too long to be processed by discord. '
                "Please visit https://chat.openai.com for details"
            )
        elif user_input.strip() == "@findproducts":
            description = (
                f'The response for your command - "{user_input.strip()}" is '
                "too long. Please set a limit to a number of products by typing "
                "@findproducts <int: limit>"
            )

        return message.channel.send(description)

    @staticmethod
    def limit_range_validation():
        description = (
            "The value is invalid. Please check if you provided a number "
            "between 1 and 10"
        )

        return description

    @staticmethod
    def limit_value_validation():
        description = (
            "The value is invalid. Please check if you provided an approptiate number "
        )

        return description

    @staticmethod
    def no_category_valdation():
        description = "No category/wrong category has been provided"

        return description

    @staticmethod
    def no_product_valdation():
        description = "No such product exists. Check data you have provided"

        return description

    @staticmethod
    def no_country_validation():
        description = "No such country exists. Check data you have provided"

        return description
