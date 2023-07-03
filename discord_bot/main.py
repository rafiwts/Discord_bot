import discord
from discord.ext import commands

from dotenv import load_dotenv
import os
import logging
import requests
import json

load_dotenv()

handler = logging.FileHandler(filename='discord.log',
                              encoding='utf-8',
                              mode='w')
   
intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix='!', intents=intents)


def get_json():
      response = requests.get('https://zenquotes.io/api/quotes/')
      json_data = json.loads(response.text)
      quote = f"{json_data[0]['q']} by {json_data[0]['a']}"
      return quote


@client.event
async def on_ready() -> None:
      print(f'Logged in as {client.user} (ID: {client.user.id})')
      print('--------------------------------------------')


@client.command()
async def hello(command) -> None:
      await command.channel.send('Hello!')


@client.event
async def on_message(message) -> None:
      content = message.content
      
      if message.author == client.user:
            return

      if content.startswith('$findme'):
            quote = get_json()
            await message.channel.send(quote)
      
      if content.startswith('!'):
            await message.channel.send('Hello!')

client.run(os.getenv('TOKEN'), log_handler=handler)