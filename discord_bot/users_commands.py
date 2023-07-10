import datetime


def new_session_command(context, current_session):
    current_session.is_active = True
    current_session.start_time = context.message.created_at.timestamp()
    session_starting_time = context.message.created_at.strftime('%H:%M:%S')
    return context.send(f'New current_session started at {session_starting_time} by {current_session.user_id}')


def end_session_command(context, current_session):
    current_session.is_active = False
    current_session.finish_time = context.message.created_at.timestamp()
    duration = current_session.finish_time - current_session.start_time
    #TODO: change the display of second/minutes
    duration_in_seconds = datetime.timedelta(seconds=duration).total_seconds() 
    return context.send(f'The session ended after {round(duration_in_seconds, 2)} seconds')


def list_of_users(context, guild_id, bot):
    for guild in bot.guilds:
            if guild.name == guild_id:
                  break
      
    members = ([member.name for member in guild.members])
    print(members)
     
    return context.send(members)