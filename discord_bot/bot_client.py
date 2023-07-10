import discord
from discord.ext import commands

import server_events, users_commands
from web_responses import get_encouragement_quote
from session import Session

import os
import logging
import datetime
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')
# does not work as an environment variable
CHANNEL_ID = 1125323466921476118 
GUILD = os.getenv('DISCORD_GUILD')

handler = logging.FileHandler(filename='discord.log',
                              encoding='utf-8',
                              mode='w')
   
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

#TODO: Think about a more efficient implementation of the list
list_of_commands = ['$', '?']

session = Session(bot_id=bot.user, user_id='123')


@bot.event
async def on_ready() -> None:
      response_on_ready = server_events.return_on_ready(bot=bot, 
                                                        channel_id=CHANNEL_ID, 
                                                        guild=GUILD)
      await response_on_ready

      
@bot.event
async def on_message(message) -> None:
      #TODO: different events -> and different commands - bot should display them - we will develop it later on
      if message.author == bot.user:
            return
      
      if message.content in list_of_commands:
            response_to_message = server_events.return_on_message(message=message)
            await response_to_message

      await bot.process_commands(message)


@bot.event
async def on_typing(channel, user, when):
     response_to_typing = server_events.return_on_typing(channel=channel, 
                                                         user=user, 
                                                         when=when)
     await response_to_typing
   

@bot.command()
async def start(ctx):
      if session.is_active:
            await ctx.send('A session is already active!')
            return

      start_new_session = users_commands.new_session_command(context=ctx,
                                                             current_session=session)
      await start_new_session


@bot.command()
async def end(ctx):
      if not session.is_active:
          await ctx.send('Session is not active!')
          return
     
      end_current_session = users_commands.end_session_command(context=ctx,
                                                               current_session=session)
      await end_current_session


@bot.command()
async def users(ctx):
      users_list = users_commands.list_of_users(context=ctx,
                                   guild_id=GUILD,
                                   bot=bot,)
      await users_list


@bot.command()
async def square(ctx, arg): # The name of the function is the name of the command
    print(arg) # this is the text that follows the command
    await ctx.send(int(arg) ** 2) # ctx.send sends text in chat


@bot.command()
async def scrabblepoints(ctx, arg):
    # Key for point values of each letter
    score = {"a": 1, "c": 3, "b": 3, "e": 1, "d": 2, "g": 2,
         "f": 4, "i": 1, "h": 4, "k": 5, "j": 8, "m": 3,
         "l": 1, "o": 1, "n": 1, "q": 10, "p": 3, "s": 1,
         "r": 1, "u": 1, "t": 1, "w": 4, "v": 4, "y": 4,
         "x": 8, "z": 10}
    points = 0
    # Sum the points for each letter
    for c in arg:
        points += score[c]
    await ctx.send(points)

bot.run(TOKEN, log_handler=handler)