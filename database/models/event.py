import peewee
import discord
from datetime import datetime

from database.models.base import DefaultDatabaseModel
from database.models import DiscordUser


class Event(DefaultDatabaseModel):
    name: str = peewee.CharField()
    created_at: int = peewee.DateTimeField(default=datetime.now())
    user: int = peewee.ForeignKeyField(
        DiscordUser, backref="events", on_delete="CASCADE"
    )
    counter: int = peewee.IntegerField(default=1)

    @classmethod
    def create_new_event(
        cls, user: peewee.ForeignKeyField, sent_message: discord.Message = None
    ):
        return cls.create(
            name=sent_message.content, cteated_at=sent_message.created_at, user=user
        )

    @classmethod
    def increment_counter(
        cls,
        user: discord.Member,
        sent_message: discord.Message,
        counter: peewee.IntegerField,
    ):
        return cls.update(counter=counter).where(
            (cls.name == sent_message.content) & (cls.user == user)
        )

    def __str__(self) -> str:
        return f"Event {self.id}"
