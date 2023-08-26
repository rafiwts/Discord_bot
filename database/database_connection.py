from database.models.base import psql_database
from database.models import DiscordUser, Message, Command, Event, Reaction, BotUser


def create_tables():
      with psql_database:
            psql_database.create_tables([DiscordUser, 
                                         Message, 
                                         Command, 
                                         Event, 
                                         Reaction,
                                         BotUser])
            

def drop_tables():
      with psql_database:
            psql_database.drop_tables([DiscordUser,
                                       Message,
                                       Command,
                                       Event,
                                       Reaction,
                                       BotUser])