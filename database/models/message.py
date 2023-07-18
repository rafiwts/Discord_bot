import peewee
from datetime import datetime

from database.models.base import DefaultDatabaseModel
from database.models import DiscordUser


class Message(DefaultDatabaseModel):
    discord_id = peewee.IntegerField(unique=True)
    content = peewee.TextField(null=False)
    created_at = peewee.DateTimeField(default=datetime.now)
    edited_at = peewee.DateTimeField(default=datetime.now)
    user = peewee.ForeignKeyField(DiscordUser, 
                                  backref='messages',
                                  on_delete='CASCADE')