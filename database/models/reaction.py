import peewee
from datetime import datetime

from database.models.base import DefaultDatabaseModel
from database.models import DiscordUser, Message


class Reaction(DefaultDatabaseModel):
    user: int = peewee.ForeignKeyField(DiscordUser, 
                                       backref='reactions',
                                       on_delete='CASCADE')
    content = peewee.ForeignKeyField(Message,
                                     backref='reactions',
                                     on_delete='CASCADE')
    added_at: int = peewee.DateTimeField(default=datetime.now)
    edited_at: int = peewee.DateTimeField(default=datetime.now)
    reaction_counter: int = peewee.IntegerField(default=0)
   
    
    def __str__(self) -> str:
        return f'Message {self.id}'