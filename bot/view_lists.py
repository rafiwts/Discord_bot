import os

from dotenv import load_dotenv

load_dotenv()

dict_of_actions = {1: "showevents", 2: "showcommands"}

# TODO: add an event
dict_of_events = {
    "chatgpt": "@chatgpt",
    "weather": "@checkweather",
    "encourage": "@encourageme",
    "find_item": "@finditem",
    "find_categories": "@findcategories",
    "find_products": "@findproducts",
}

dict_of_commands = {
    "joined": "!joined",
    "start": "!start",
    "session": "!session",
    "end": "!end",
    "users": "!users",
    "info": "!info",
    "square": "!square",
    "scrabblepoints": "!scrabblepoints",
}


class EventsView:
    events = dict_of_events

    @classmethod
    def askbot_event(cls):
        description = (
            f"{cls.events['chatgpt']} <user's question> - conntects "
            "discord with ChatGPT in order to process user's given command. "
        )
        return description

    @classmethod
    def weather_event(cls):
        description = (
            f"{cls.events['weather']} <country> <city> - enter the event type "
            "followed by the name of the city to receive the current "
            "weather in a given place"
        )
        return description

    @classmethod
    def encourage_event(cls):
        description = (
            f"{cls.events['encourage']} - returns a encouraging quote "
            "to make your day better :)"
        )
        return description

    @classmethod
    def find_item_by_name_event(cls):
        description = (
            f"{cls.events['find_item']} <item> - enter the event type "
            "followed by the name of the item to receive the best offers "
            "of a given product form the online store"
        )
        return description

    @classmethod
    def find_all_products_for_category_event(cls):
        description = (
            f"{cls.events['find_products']} <category> - returns all products "
            "that are available for a given category"
        )
        return description

    @classmethod
    def find_all_categories_event(cls):
        description = (
            f"{cls.events['find_categories']} - returns all product categories "
            "that are available in the online store"
        )
        return description

    @classmethod
    def find_products_with_limit_event(cls):
        description = (
            f"{cls.events['find_products']} <int:limit> - returns all products "
            "that are available for a given category (no more than 10). If no "
            "value is provided, it will not work"
        )
        return description

    @classmethod
    def return_all_events(cls):
        events = (
            f"{cls.askbot_event()}\n"
            f"{cls.weather_event()}\n"
            f"{cls.encourage_event()}\n"
            f"{cls.find_item_by_name_event()}\n"
            f"{cls.find_all_categories_event()}\n"
            f"{cls.find_all_products_for_category_event()}\n"
            f"{cls.find_products_with_limit_event()}"
        )
        return events


class CommandsView:
    commands = dict_of_commands

    @classmethod
    def joined_command(cls):
        description = (
            f"{cls.commands['joined']} - returns user's exact "
            f"date of joining the guild {os.getenv('DISCORD_GUILD')}"
        )
        return description

    @classmethod
    def start_command(cls):
        description = f"{cls.commands['start']} - begins user's session"
        return description

    @classmethod
    def session_command(cls):
        description = (
            f"{cls.commands['session']} - checks the duration " "of user's session"
        )
        return description

    @classmethod
    def end_command(cls):
        description = f"{cls.commands['end']} - ends user's session "
        return description

    @classmethod
    def users_command(cls):
        description = (
            f"{cls.commands['users']} - returns a list of "
            f"user for a guild {os.getenv('DISCORD_GUILD')}"
        )
        return description

    @classmethod
    def info_command(cls):
        description = (
            f"{cls.commands['info']} - returns a set of options "
            "you have within the server"
        )
        return description

    @classmethod
    def square_command(cls):
        description = (
            f"{cls.commands['square']} - returns a square number "
            "of an integer provided by the user"
        )
        return description

    @classmethod
    def scrabblepoints_command(cls):
        description = (
            f"{cls.commands['scrabblepoints']} - returns the number "
            "of points you get for a given word in scrabble"
        )
        return description

    @classmethod
    def return_all_commands(cls):
        commands = (
            f"{cls.info_command()}\n"
            f"{cls.joined_command()}\n"
            f"{cls.start_command()}\n"
            f"{cls.session_command()}\n"
            f"{cls.end_command()}\n"
            f"{cls.users_command()}\n"
            f"{cls.square_command()}\n"
            f"{cls.scrabblepoints_command()}\n"
        )
        return commands
