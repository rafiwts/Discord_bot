import peewee
from datetime import datetime

from database.models.base import DefaultDatabaseModel
from database.models import DiscordUser


class Event(DefaultDatabaseModel):
    discord_id = peewee.IntegerField(unique=True)
    created = peewee.DateTimeField(default=datetime.now)
    user = peewee.ForeignKeyField(DiscordUser,
                                  backref='events',
                                  on_delete='CASCADE')