import discord
from discord.ext import commands

from web_responses import get_encouragement_quote
from user_choices import display_quotation_choice

import os
import logging
import datetime
from dotenv import load_dotenv
from bot_session import Session

load_dotenv()
TOKEN = os.getenv('TOKEN')
CHANNEL_ID = 1125323466921476118 # does not work as an environment variable
GUILD = os.getenv('DISCORD_GUILD')

handler = logging.FileHandler(filename='discord.log',
                              encoding='utf-8',
                              mode='w')
   
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

session = Session(bot_id=bot.user, user_id='123')


@bot.event
async def on_ready() -> None:
      print(f'Hi Everyone! {bot.user} has just connected to {GUILD}')
      channel = bot.get_channel(CHANNEL_ID)
      await channel.send (f'Hi Everyone! {bot.user} has just connected to {GUILD}')

      
@bot.event
async def on_message(message) -> None:
      if message.author == bot.user:
            return

      if message.content.startswith('$'):
            choices = ['encourage', 'disappoint']
            choice = display_quotation_choice(choices)
            await message.channel.send(choice)
      
      if message.content.startswith('?'):
            await message.channel.send('Hello!')
      
      await bot.process_commands(message)


@bot.command()
async def start(ctx):
      if session.is_active:
            await ctx.send('A session is already active!')
            return
      
      
      session.is_active = True
      session.start_time = ctx.message.created_at.timestamp()
      session_starting_time = ctx.message.created_at.strftime('%H:%M:%S')
      await ctx.send(f'New session started at {session_starting_time} by {session.user_id}')


@bot.command()
async def end(ctx):
      if not session.is_active:
          await ctx.send('Session is not active!')
          return
     
      session.is_active = False
      session.finish_time = ctx.message.created_at.timestamp()
      duration = session.finish_time - session.start_time
      duration_in_seconds= datetime.timedelta(seconds=duration).total_seconds()
      await ctx.send(f'The session ended after {round(duration_in_seconds, 2)} seconds')


@bot.command()
async def users(ctx, args):
      for guild in bot.guilds:
            if guild.name == GUILD:
                  break
      
      members = ([member.name for member in guild.members])
      print(members)
     
      await ctx.send(args)


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