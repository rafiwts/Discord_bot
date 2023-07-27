import discord

import logging
from typing import Coroutine

from bot.client import DiscordBot
from bot.session import Session
from bot.server_events import ServerEvents
from bot.users_commands import UserCommands
from database.database_connection import create_tables
from settings import CHANNEL_ID, GUILD, TOKEN

intents = discord.Intents.default()
intents.message_content = True

handler = logging.FileHandler(filename='discord.log',
                              encoding='utf-8',
                              mode='w')

bot = DiscordBot(command_prefix='!', intents=intents)

bot.initialize()
#FIXME: find a better solutrion to it - creating session and then adding a parameter
new_session = Session(bot_id=bot.user)
new_session.user_id=discord.Member.name

create_tables()


@bot.event
async def on_ready() -> None:
      response_to_ready = ServerEvents.return_on_ready(bot=bot, 
                                                       channel_id=CHANNEL_ID, 
                                                       guild=GUILD)
      await response_to_ready
      await bot.process_bot(bot=bot,
                            guild=GUILD)


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
async def on_message(message: discord.Message) -> Coroutine:
      #TODO: Think about a more efficient implementation of the list
      list_of_events = ['$', '?', 'showevents', 'showcommands']

      if message.author == bot.user:
            return
      elif message.content.startswith('!') and len(message.content) > 1:
            await bot.process_commands(message)
      elif message.content.startswith(tuple(list_of_events)):
            response_to_message = ServerEvents.return_on_message(message=message)
            await response_to_message
            await bot.process_message(message)
      else:
            await bot.process_message(message)


@bot.event
async def on_message_edit(old_message: discord.Message, new_message: discord.Message) -> Coroutine:
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
async def on_raw_reaction_add(reaction):
      await bot.process_reaction(reaction)


@bot.event
async def on_raw_reaction_remove(reaction):
      await bot.process_reaction(reaction)


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
      #FIXME: how to call a class only within a function 
      if new_session.is_active:
            await ctx.send('A session is already active!')
            return
      
      new_session.user_id = ctx.author
      
      start_new_session = UserCommands.new_session_command(context=ctx,
                                                           new_session=new_session)
      await start_new_session


@bot.command()
async def session(ctx):
      if not new_session.is_active:
            await ctx.send('Session is not active')
            return

      duration_of_session = UserCommands.lasting_session(context=ctx,
                                                         current_session=new_session)
      await duration_of_session


@bot.command()
async def end(ctx):
      if not new_session.is_active:
            await ctx.send('Session is not active!')
            return

      end_current_session = UserCommands.end_session_command(context=ctx,
                                                             current_session=new_session)
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


if __name__ == '__main__':
      bot.run(TOKEN, log_handler=handler)