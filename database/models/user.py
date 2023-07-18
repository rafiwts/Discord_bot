import peewee
from datetime import datetime

from database.models.base import DefaultDatabaseModel


class DiscordUser(DefaultDatabaseModel):
    username = peewee.CharField(max_length=50, 
                                null=False)
    discord_id = peewee.IntegerField(unique=True)
    guildname = peewee.CharField(max_length=50)
    created_at = peewee.DateTimeField(default=datetime.now)
    joined_at = peewee.DateTimeField(default=datetime.now)
    is_bot = peewee.BooleanField()