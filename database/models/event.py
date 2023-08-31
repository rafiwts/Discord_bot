import peewee
import discord
from datetime import datetime

from database.models.base import DefaultDatabaseModel
from database.models import DiscordUser


class Event(DefaultDatabaseModel):
    content: peewee.CharField = peewee.CharField(null=True)
    created_at: peewee.DateTimeField = peewee.DateTimeField(default=datetime.now())
    user: peewee.ForeignKeyField = peewee.ForeignKeyField(
        DiscordUser, backref="events", on_delete="CASCADE"
    )
    counter: peewee.IntegerField = peewee.IntegerField(default=1)

    @classmethod
    def create_new_event(
        cls, user: peewee.ForeignKeyField, sent_message: discord.Message = None
    ):
        if sent_message:
            return cls.create(
                content=sent_message.content,
                created_at=sent_message.created_at,
                user=user,
            )

        return cls.create(user=user)

    @classmethod
    def increment_counter(
        cls,
        user: discord.Member,
        sent_message: discord.Message,
        counter: peewee.IntegerField,
    ):
        return cls.update(counter=counter).where(
            (cls.content == sent_message.content) & (cls.user == user)
        )

    def __str__(self) -> str:
        return f"Event {self.id}"
