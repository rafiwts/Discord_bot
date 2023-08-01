import peewee
from datetime import datetime

from database.models.base import DefaultDatabaseModel
from database.models import DiscordUser
#FIXME: cannot import from the 'init' file
from database.models.command import Command


class Message(DefaultDatabaseModel):
    content: str = peewee.TextField(null=False)
    created_at: int = peewee.DateTimeField(default=datetime.now)
    edited_at: int = peewee.DateTimeField(null=True)
    user: int = peewee.ForeignKeyField(DiscordUser,
                                       backref='messages',
                                       on_delete='CASCADE')
    command: int = peewee.ForeignKeyField(Command,
                                          backref='messages',
                                          on_delete='CASCADE')
    reaction_counter: int = peewee.IntegerField(default=0)

    @classmethod
    def create_new_message(cls, content: peewee.TextField,
                                first_created: peewee.DateTimeField, 
                                user: peewee.ForeignKeyField,
                                command: peewee.ForeignKeyField):
        return cls.create(content=content,
                          created_at=first_created,
                          user=user,
                          command=command)
    
    def __str__(self) -> str:
        return f'Message {self.id}'