import peewee
from datetime import datetime

import discord

from database.models.base import DefaultDatabaseModel
from database.models import DiscordUser


class Command(DefaultDatabaseModel):
    content: peewee.TextField = peewee.TextField(null=False)
    created_at: peewee.DateTimeField = peewee.DateTimeField(
        default=datetime.now(), null=False
    )
    edited_at: peewee.DateTimeField = peewee.DateTimeField(null=True)
    user: peewee.ForeignKeyField = peewee.ForeignKeyField(
        DiscordUser, backref="commands", on_delete="CASCADE"
    )
    command_counter: peewee.IntegerField = peewee.IntegerField(default=1, null=False)

    @classmethod
    def create_new_command(cls, message: discord.Message, user: peewee.ForeignKeyField):
        return cls.create(
            content=message.content, created_at=message.created_at, user=user
        )

    @classmethod
    def increment_counter(
        cls,
        command_counter: peewee.IntegerField,
        message: discord.Message,
        discord_user: peewee.ForeignKeyField,
    ):
        return cls.update(
            edited_at=message.created_at, command_counter=command_counter
        ).where((cls.content == message.content) & (cls.user == discord_user))

    def __str__(self) -> str:
        return self.content
