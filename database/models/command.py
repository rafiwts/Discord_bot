import peewee
from datetime import datetime

import discord

from database.models.base import DefaultDatabaseModel
from database.models import DiscordUser


class Command(DefaultDatabaseModel):
    content: str = peewee.TextField(null=False)
    first_created: int = peewee.DateTimeField(default=datetime.now(), null=False)
    last_updated: int = peewee.DateTimeField(default=datetime.now(), null=True)
    user: int = peewee.ForeignKeyField(DiscordUser, 
                                       backref='commands',
                                       on_delete='CASCADE')
    command_counter: int = peewee.IntegerField(default=1, null=False)

    @classmethod
    def create_new_command(cls, content: peewee.TextField,
                                first_created: peewee.DateTimeField, 
                                user: peewee.ForeignKeyField):
        return cls.create(content=content,
                          first_created=first_created,
                          user=user)
    
    @classmethod
    def increment_counter(cls, last_updated: peewee.DateTimeField,
                               command_counter: peewee.IntegerField,
                               message: discord.Message,
                               discord_user: peewee.ForeignKeyField):
        return cls.update(last_updated=last_updated,
                          command_counter=command_counter)\
                          .where((cls.content==message) &
                                 (cls.user==discord_user))

    def __str__(self) -> str:
        return self.content