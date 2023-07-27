import peewee
from datetime import datetime

from database.models.base import DefaultDatabaseModel


class DiscordUser(DefaultDatabaseModel):
    username: str = peewee.CharField(max_length=50, 
                                     null=False,
                                     unique=True)
    guildname: str = peewee.CharField(max_length=50)
    created_at: int = peewee.DateTimeField(default=datetime.now())
    joined_at: int = peewee.DateTimeField(default=datetime.now())
    is_bot: bool = peewee.BooleanField(default=False)
    is_admin: peewee.BooleanField = peewee.BooleanField(default=False)

    def __str__(self) -> str:
        return self.username