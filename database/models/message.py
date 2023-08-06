import peewee
from datetime import datetime

from database.models.base import DefaultDatabaseModel
from database.models import DiscordUser
#FIXME: cannot import from the 'init' file
from database.models.command import Command, DiscordUser


class Message(DefaultDatabaseModel):
    discord_id = peewee.BigIntegerField()
    content: str = peewee.TextField(null=False)
    created_at: int = peewee.DateTimeField(default=datetime.now())
    edited_at: int = peewee.DateTimeField(null=True, default=None)
    user: int = peewee.ForeignKeyField(DiscordUser,
                                       backref='messages',
                                       on_delete='CASCADE')
    command: int = peewee.ForeignKeyField(Command,
                                          backref='messages',
                                          on_delete='SET NULL',
                                          null=True)
    reaction_counter: int = peewee.IntegerField(default=0)

    @classmethod
    def create_new_message(cls, discord_id: peewee.BigIntegerField,
                                content: peewee.TextField,
                                first_created: peewee.DateTimeField, 
                                user: peewee.ForeignKeyField,
                                command: peewee.ForeignKeyField = None):
        return cls.create(discord_id=discord_id,
                          content=content,
                          created_at=first_created,
                          user=user,
                          command=command)
    
    @classmethod
    def edit_message(cls, discord_id: peewee.BigIntegerField,
                          new_content: peewee.TextField = None, 
                          edited_at: peewee.DateTimeField = None,
                          reaction_counter: peewee.IntegerField = None):
        if reaction_counter:
            return cls.update(reaction_counter=reaction_counter)\
                      .where(cls.discord_id==discord_id).execute()
        
        return cls.update(content=new_content,
                          edited_at=edited_at).where(cls.discord_id==discord_id).execute()

    def __str__(self) -> str:
        return f'Message {self.id}'