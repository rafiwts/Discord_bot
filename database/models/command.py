import peewee
from datetime import datetime

from database.models.base import DefaultDatabaseModel
from database.models import DiscordUser


class Command(DefaultDatabaseModel):
    discord_id = peewee.IntegerField(unique=True)
    content = peewee.TextField(null=False)
    created = peewee.DateTimeField(default=datetime.now)
    updated = peewee.DateTimeField(default=datetime.now)
    user = peewee.ForeignKeyField(DiscordUser, 
                                  backref='commands',
                                  on_delete='CASCADE')