import discord
from discord.ext import commands

from web_responses import get_encouragement_quote
from user_choices import display_quotation_choice

from dotenv import load_dotenv
import os
import logging

load_dotenv()

handler = logging.FileHandler(filename='discord.log',
                              encoding='utf-8',
                              mode='w')
   
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready() -> None:
      print(f'Logged in as {bot.user} (ID: {bot.user.id})')
      print('------------------------------------------------------')


@bot.event
async def on_message(message) -> None:
      if message.author == bot.user:
            return

      if message.content.startswith('$quote'):
            choices = ['encourage', 'disappoint']
            choice = display_quotation_choice(choices)
            await message.channel.send(choice)

            if message.content.startswith('q'):
                  quote = get_encouragement_quote()
                  await message.channel.send(quote)
      
      if message.content.startswith('?'):
            await message.channel.send('Hello!')
      
      await bot.process_commands(message)

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

bot.run(os.getenv('TOKEN'), log_handler=handler)