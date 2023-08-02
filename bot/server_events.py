from dotenv import load_dotenv
import os
#TODO: change it into a class --> properties will be fine I believe

load_dotenv()


class ServerEvents:
    #TODO: maybe they will be necessary later on
    token: int = os.getenv('TOKEN')
    #FIXME: does not work as an environment variable
    channel_id: int = os.getenv('CHANNEL_ID')
    guild: str = os.getenv('DISCORD_GUILD')

    def return_on_ready(bot, guild, channel_id):
        channel = bot.get_channel(channel_id)
        return channel.send (f'''Hi Everyone! {bot.user} has just connected to {guild}
Below you will find a list of commands that you can use:
showevents: returns a list of actions
showcommands: returns a list of commands''')

    def return_on_message(message):
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

    def return_on_editing(sent_message, edited_message, user):
        return edited_message.channel.send(f'{user} has edited the message')

    def return_on_deleting(message):
        return message.channel.send(f'{message.author} has deleted the message')
                                        
    def return_on_typing(channel, user, when):
        return channel.send(f'Hi {user}! How can I help you?')
    
    def return_on_joining(member, channel):
        return channel.send(f'a new user {member} has entered the chat')
    
    def return_on_removing(member, channel):
        return channel.send(f'{member} has been removed')
    