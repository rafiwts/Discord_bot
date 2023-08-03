import peewee
from datetime import datetime

from database.models.base import DefaultDatabaseModel
from database.models import DiscordUser
#FIXME: cannot import from the 'init' file
from database.models.command import Command, DiscordUser


class Message(DefaultDatabaseModel):
    message_id = peewee.BigIntegerField(primary_key=True)
    content: str = peewee.TextField(null=False)
    created_at: int = peewee.DateTimeField(default=datetime.now())
    edited_at: int = peewee.DateTimeField(null=True)
    user: int = peewee.ForeignKeyField(DiscordUser,
                                       backref='messages',
                                       on_delete='CASCADE')
    command: int = peewee.ForeignKeyField(Command,
                                          backref='messages',
                                          on_delete='SET NULL',
                                          null=True)
    reaction_counter: int = peewee.IntegerField(default=0)

    @classmethod
    def create_new_message(cls, message_id: peewee.BigIntegerField,
                                content: peewee.TextField,
                                first_created: peewee.DateTimeField, 
                                user: peewee.ForeignKeyField,
                                command: peewee.ForeignKeyField = None):
        return cls.create(message_id=message_id,
                          content=content,
                          created_at=first_created,
                          user=user,
                          command=command)
    
    @classmethod
    def edit_message(cls, message_id: peewee.BigIntegerField,
                          new_content: peewee.TextField, 
                          edited_at: peewee.DateTimeField):
        
        return cls.update(content=new_content,
                          edited_at=edited_at).where(cls.message_id==message_id).execute()
 
    def __str__(self) -> str:
        return f'Message {self.id}'