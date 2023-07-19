import peewee
from datetime import datetime

from database.models.base import DefaultDatabaseModel
from database.models import DiscordUser


class Event(DefaultDatabaseModel):
    created: int = peewee.DateTimeField(default=datetime.now)
    user: int = peewee.ForeignKeyField(DiscordUser,
                                  backref='events',
                                  on_delete='CASCADE')
    
    def __str__(self) -> str:
        return f'Event {self.id}'