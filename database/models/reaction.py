import peewee
from datetime import datetime

from database.models.base import DefaultDatabaseModel
from database.models import DiscordUser, Message


class Reaction(DefaultDatabaseModel):
    user_from: int = peewee.ForeignKeyField(DiscordUser, 
                                            backref='senders',
                                            on_delete='CASCADE')
    user_to: int = peewee.ForeignKeyField(DiscordUser,
                                          backref='recipients',
                                          on_delete='CASCADE')
    message = peewee.ForeignKeyField(Message,
                                     backref='reactions',
                                     on_delete='CASCADE')
    added_at: int = peewee.DateTimeField(default=datetime.now)
    edited_at: int = peewee.DateTimeField(default=datetime.now)
   
    def __str__(self) -> str:
        return f'Message {self.id}'