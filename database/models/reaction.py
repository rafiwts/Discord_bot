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
    message:int = peewee.ForeignKeyField(Message,
                                     to_field='message_id'
                                     backref='reactions'
                                     on_delete='CASCADE')
    added_at: int = peewee.DateTimeField(default=datetime.now())
    edited_at: int = peewee.DateTimeField(default=datetime.now())
   
    @classmethod
    def create_new_reaction(cls, user_from: peewee.ForeignKeyField,
                                 user_to: peewee.ForeignKeyField, 
                                 message: peewee.ForeignKeyField):
        return cls.create(user_from=user_from,
                          user_to=user_to,
                          message=message)
    
    def __str__(self) -> str:
        return f'Message {self.id}'