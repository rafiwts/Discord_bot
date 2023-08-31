import os
import time
import discord
from dotenv import load_dotenv

load_dotenv()


# TODO: change it into several classes
class UserCommands:
    # maybe they will be necessary later on
    token: int = os.getenv("TOKEN")
    # does not work as an environment variable
    channel_id: int = os.getenv("CHANNEL_ID")
    guild: str = os.getenv("DISCORD_GUILD")

    def new_session_command(context, new_session):
        new_session.is_active = True
        new_session.start_time = time.time()
        session_starting_time = context.message.created_at.strftime("%H:%M:%S")
        return context.send(
            f"New session started at {session_starting_time} by {new_session.user_id}"
        )

    def lasting_session(context, current_session):
        return_session = current_session.duration_of_session
        return context.send(f"The session lasts {round(return_session, 2)} seconds")

    def end_session_command(context, current_session):
        current_session.is_active = False
        current_session.finish_time = time.time()
        duration = current_session.finish_time - current_session.start_time
        return context.send(f"The session ended after {round(duration, 2)} seconds")

    def list_of_users(context, guild_id: discord.Guild, bot):
        for guild in bot.guilds:
            if guild.name == guild_id:
                break
        print(guild.members)

        members = [member for member in guild.members]

        return context.send(members)

    def return_square(context, users_choice):
        try:
            print(users_choice)
            return context.send(int(users_choice) ** 2)
        except ValueError:
            print(f"Error! {users_choice} is not a valid number")
            return context.send(f'Error! "{users_choice}" is not a valid number')

    def get_scrabble_points(context, users_choice):
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
        except:
            print(f"Error! {users_choice} is not a word")
            return context.send(f'Error! "{users_choice}" is not a valid word')
