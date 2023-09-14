import time

import discord
from discord.ext import commands
from dotenv import load_dotenv

from .session import Session

load_dotenv()


class UserCommands:
    @staticmethod
    def display_info_command(context: discord.Message) -> str:
        return context.send(
            """Below you will find a list of commands that you can use:
showevents: returns a list of actions
showcommands: returns a list of commands"""
        )

    @staticmethod
    def new_session_command(context: discord.Message, new_session: Session) -> str:
        new_session.is_active = True
        new_session.start_time = time.time()
        session_starting_time = context.message.created_at.strftime("%H:%M:%S")
        return context.send(
            f"New session started at {session_starting_time} by {new_session.user_id}"
        )

    @staticmethod
    def lasting_session(context: discord.Message, current_session: Session) -> str:
        return_session = current_session.duration_of_session
        return context.send(f"The session lasts {round(return_session, 2)} seconds")

    @staticmethod
    def end_session_command(context: discord.Message, current_session: Session) -> str:
        current_session.is_active = False
        current_session.finish_time = time.time()
        duration = current_session.finish_time - current_session.start_time
        return context.send(f"The session ended after {round(duration, 2)} seconds")

    @staticmethod
    def list_of_users(
        context: discord.Message, guild_id: discord.Guild, bot: commands.Bot
    ) -> str:
        for guild in bot.guilds:
            if guild.name == guild_id:
                break
        print(guild.members)

        members = [member for member in guild.members]

        return context.send(members)

    @staticmethod
    def return_square(context: discord.Message, users_choice: int) -> str:
        try:
            print(users_choice)
            return context.send(int(users_choice) ** 2)
        except ValueError:
            print(f"Error! {users_choice} is not a valid number")
            return context.send(f'Error! "{users_choice}" is not a valid number')

    @staticmethod
    def get_scrabble_points(context: discord.Message, users_choice: str) -> str:
        score = {
            "a": 1,
            "c": 3,
            "b": 3,
            "e": 1,
            "d": 2,
            "g": 2,
            "f": 4,
            "i": 1,
            "h": 4,
            "k": 5,
            "j": 8,
            "m": 3,
            "l": 1,
            "o": 1,
            "n": 1,
            "q": 10,
            "p": 3,
            "s": 1,
            "r": 1,
            "u": 1,
            "t": 1,
            "w": 4,
            "v": 4,
            "y": 4,
            "x": 8,
            "z": 10,
        }
        total_points = 0
        try:
            for letter in users_choice:
                total_points += score[letter]
            print(f"{users_choice} has {total_points} points")
            return context.send(f"{users_choice} has {total_points} points")
        except TypeError:
            print(f"Error! {users_choice} is not a word")
            return context.send(f'Error! "{users_choice}" is not a valid word')
