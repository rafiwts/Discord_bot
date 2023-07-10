#TODO: to be expanded using other functionalities
def return_on_typing(channel, user, when):
     return channel.send(f'Hi {user}! How can I help {when}')


def return_on_ready(bot, guild, channel_id):
    print(f'Hi Everyone! {bot.user} has just connected to {guild}')
    channel = bot.get_channel(channel_id)
    return channel.send (f'Hi Everyone! {bot.user} has just connected to {guild}')


def return_on_message(message):
    if message.content.startswith('$'):
        choices = ['encourage', 'disappoint']
        return message.channel.send(choices)
      
    if message.content.startswith('?'):
        return message.channel.send('Hello!')
      
    