import discord
from discord.ext import commands

from server_events import ServerEvents
from users_commands import UserCommands
from web_responses import get_encouragement_quote
from session import Session

import os
import logging
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

session = Session(bot_id=bot.user, user_id='123')


@bot.event
async def on_ready() -> None:
      response_to_ready = ServerEvents.return_on_ready(bot=bot, 
                                                       channel_id=CHANNEL_ID, 
                                                       guild=GUILD)
      await response_to_ready


@bot.event
async def on_member_join(member):
      response_to_joining = ServerEvents.return_on_joining(member=member,
                                                           channel=CHANNEL_ID)
      await response_to_joining


@bot.event
async def on_member_remove(member):
      response_to_removing = ServerEvents.return_on_removing(member=member,
                                                             channel=CHANNEL_ID)
      await response_to_removing


@bot.event
async def on_message(message) -> None:
      #TODO: different events -> and different commands - bot should display them - we will develop it later on
      #TODO: Think about a more efficient implementation of the list
      list_of_commands = ['$', '?', 'showevents', 'showcommands']

      if message.author == bot.user:
            return
      
      if message.content in list_of_commands:
            response_to_message = ServerEvents.return_on_message(message=message)
            await response_to_message

      await bot.process_commands(message)


@bot.event
async def on_message_edit(old_message, new_message):
      user = old_message.author
      response_to_edditing = ServerEvents.return_on_editing(old_message=old_message,
                                                            new_message=new_message,
                                                            user=user)
      await response_to_edditing


@bot.event
async def on_message_delete(message):
      response_to_deleting = ServerEvents.return_on_deleting(message=message)
      await response_to_deleting


@bot.event
async def on_typing(channel, user, when):
     response_to_typing = ServerEvents.return_on_typing(channel=channel, 
                                                        user=user, 
                                                        when=when)
     await response_to_typing


@bot.command()
async def joined(ctx, *, member: discord.Member):
    await ctx.send(f'{member} joined on {member.joined_at}')


@bot.command()
async def start(ctx):
      if session.is_active:
            await ctx.send('A session is already active!')
            return

      start_new_session = UserCommands.new_session_command(context=ctx,
                                                           current_session=session)
      await start_new_session


@bot.command()
async def end(ctx):
      if not session.is_active:
          await ctx.send('Session is not active!')
          return
     
      end_current_session = UserCommands.end_session_command(context=ctx,
                                                             current_session=session)
      await end_current_session


@bot.command()
async def users(ctx):
      users_list = UserCommands.list_of_users(context=ctx,
                                              guild_id=GUILD,
                                              bot=bot)
      await users_list


@bot.command()
async def square(ctx, arg):
      return_square_number = UserCommands.return_square(context=ctx,
                                                        users_choice=arg)
      await return_square_number

      
@bot.command()
async def scrabblepoints(ctx, arg):
      return_points = UserCommands.get_scrabble_points(context=ctx,
                                                       users_choice=arg)
      await return_points


if __name__=='__main__':
      bot.run(TOKEN, log_handler=handler)