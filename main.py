import discord

import logging

from bot.client import DiscordBot
from bot.session import Session
from bot.server_events import ServerEvents
from bot.users_commands import UserCommands
from bot.view_lists import (dict_of_actions, 
                            dict_of_events)
from database.database_connection import create_tables
from settings import (CHANNEL_ID, 
                      GUILD, 
                      TOKEN)

intents = discord.Intents.default()
intents.message_content = True

handler = logging.FileHandler(filename='discord.log',
                              encoding='utf-8',
                              mode='w')

bot = DiscordBot(command_prefix='!', intents=intents)

bot.initialize()
new_session = Session(bot_id=bot.user)
new_session.user_id=discord.Member.name

create_tables()


@bot.event
async def on_ready() -> None:
      response_to_ready = ServerEvents.return_on_ready(bot, 
                                                       GUILD, 
                                                       CHANNEL_ID)
      await response_to_ready
      await bot.process_bot(bot,
                            GUILD)


@bot.event
async def on_member_join(member) -> None: 
      response_to_joining = ServerEvents.return_on_joining(member,
                                                           CHANNEL_ID)                                          
      await response_to_joining
      await bot.process_user(member,
                             GUILD)
      

@bot.event
async def on_member_remove(member) -> None:
      response_to_removing = ServerEvents.return_on_removing(member,
                                                             CHANNEL_ID)
      await response_to_removing
      await bot.process_user(member,
                             GUILD)
      

@bot.event
async def on_member_update(before, after) -> None:
      response_to_updating = ServerEvents.return_on_updating(before,
                                                             CHANNEL_ID)
      await response_to_updating
      await bot.process_user(before,
                             after,
                             GUILD)


@bot.event
async def on_member_ban(guild, user) -> None:
      response_to_banning = ServerEvents.return_on_banning(guild,
                                                           user,
                                                           CHANNEL_ID)
      await response_to_banning
      await bot.process_ban(user, guild)      
      

@bot.event
async def on_member_unban(guild, user) -> None:
      response_to_unbanning = ServerEvents.return_on_unbanning(guild,
                                                               user,
                                                               CHANNEL_ID)
      await response_to_unbanning
      await bot.process_unban(user,
                              guild)


@bot.event
async def on_message(message: discord.Message) -> None:
      if message.author == bot.user:
            return
      #TODO: if something is not a command, do not process it as a command - it accepts all inputs with ! larger than 1  
      elif message.content.startswith('!') and len(message.content) > 1:
            await bot.process_commands(message)
      elif message.content.startswith(tuple(dict_of_actions.values())):
            response_to_message = ServerEvents.return_on_message(message)
            await response_to_message
            await bot.process_event(message)
      elif message.content.startswith(tuple(dict_of_events.values())):
            response_to_event = ServerEvents.return_on_event(message)
            await response_to_event
            await bot.process_event(message)
      else:
            await bot.process_message(message)


@bot.event
async def on_message_edit(sent_message: discord.Message, edited_message: discord.Message) -> None:
      user = sent_message.author
      response_to_edditing = ServerEvents.return_on_editing(sent_message,
                                                            edited_message,
                                                            user)
      await response_to_edditing
      await bot.edit_message(sent_message,
                             edited_message)


@bot.event
async def on_message_delete(message) -> None:
      response_to_deleting = ServerEvents.return_on_deleting(message)
      await response_to_deleting
      await bot.delete_message(message)


@bot.event
async def on_raw_reaction_add(reaction):
      await bot.process_reaction(reaction)


@bot.event
async def on_raw_reaction_remove(reaction):
      await bot.process_reaction(reaction)


@bot.event
async def on_typing(channel, user, when) -> None:
      response_to_typing = ServerEvents.return_on_typing(channel, user)
      await response_to_typing


@bot.command()
async def joined(ctx, *, member: discord.Member) -> None:
      await ctx.send(f'{member} joined on {member.joined_at}')


@bot.command()
async def start(ctx) -> None:
      if new_session.is_active:
            await ctx.send('A session is already active!')
            return
      
      new_session.user_id = ctx.author
      
      start_new_session = UserCommands.new_session_command(ctx, new_session)
      await start_new_session


@bot.command()
async def session(ctx) -> None:
      if not new_session.is_active:
            await ctx.send('Session is not active')
            return

      duration_of_session = UserCommands.lasting_session(ctx, new_session)
      await duration_of_session


@bot.command()
async def end(ctx) -> None:
      if not new_session.is_active:
            await ctx.send('Session is not active!')
            return

      end_current_session = UserCommands.end_session_command(ctx, new_session)
      await end_current_session


@bot.command()
async def users(ctx) -> None:
      users_list = UserCommands.list_of_users(ctx,
                                              GUILD,
                                              bot)
      
      await users_list


@bot.command()
async def square(ctx, arg) -> None:
      return_square_number = UserCommands.return_square(ctx, arg)
      await return_square_number

      
@bot.command()
async def scrabblepoints(ctx, arg) -> None:
      return_points = UserCommands.get_scrabble_points(ctx, arg)
      await return_points


if __name__ == '__main__':
      bot.run(TOKEN, log_handler=handler)