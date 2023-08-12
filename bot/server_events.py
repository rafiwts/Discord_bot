import discord
from discord.ext import commands

class ServerEvents:

    @classmethod
    def return_on_ready(cls, bot: commands.Bot, 
                             guild: discord.Guild, 
                             channel_id: int):
        channel = bot.get_channel(channel_id)
        return channel.send (f'''Hi Everyone! {bot.user} has just connected to {guild}
Below you will find a list of commands that you can use:
showevents: returns a list of actions
showcommands: returns a list of commands''')

    @classmethod
    def return_on_message(cls, message: discord.Message):
        if message.content.strip() == 'showevents':
            #TODO: after finishing complete the list
            list_of_actions = ['encourage', 'disappoint']
            return message.channel.send(list_of_actions)
        
        if message.content.strip() == 'showcommands':
            #TODO: after finishing complete the list
            list_of_commands = '''A list of commands
'''
            return message.channel.send(list_of_commands)
 
        if message.content.strip() == '$':
            choices = ['encourage', 'disappoint']
            return message.channel.send(choices)

        if message.content.strip()  == '?':
            return message.channel.send('Hello!')

    @classmethod
    def return_on_editing(cls, sent_message: discord.Message, 
                               edited_message: discord.Message, 
                               user: discord.Member):
        return edited_message.channel.send(f'{user} has edited the message')

    @classmethod
    def return_on_deleting(cls, message: discord.Message):
        return message.channel.send(f'{message.author} has deleted the message')

    @classmethod                                    
    def return_on_typing(cls, channel: discord.TextChannel, 
                              user: discord.Member):
        return channel.send(f'Hi {user}! How can I help you?')
    
    @classmethod
    def return_on_joining(cls, member: discord.Message, 
                               channel: discord.TextChannel):
        return channel.send(f'a new user {member} has entered the chat')
    
    @classmethod
    def return_on_removing(cls, member: discord.Member, 
                                channel: discord.TextChannel):
        return channel.send(f'{member} has been removed')
    
    @classmethod
    def return_on_updating(cls, old_user: discord.Member,
                                channel: discord.TextChannel):
        return channel.send(f'{old_user} has updated their profile')
    
    @classmethod
    def return_on_banning(cls, guild: discord.Guild, 
                               member: discord.Member,
                               channel: discord.TextChannel):
        return channel.send(f'{member} has been temporarily banned from {guild}')
    
    @classmethod
    def return_on_unbanning(cls, guild: discord.Guild,
                                 member: discord.Member,
                                 channel:discord.TextChannel):
        return channel.send(f'{member} has been unbanned from {guild}')