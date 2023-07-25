import peewee
from datetime import datetime

from database.models.base import DefaultDatabaseModel
from database.models import DiscordUser


class Command(DefaultDatabaseModel):
    content: str = peewee.TextField(null=False)
    first_created: int = peewee.DateTimeField(default=datetime.now)
    last_updated: int = peewee.DateTimeField(default=datetime.now, null=True)
    user: int = peewee.ForeignKeyField(DiscordUser, 
                                       backref='commands',
                                       on_delete='CASCADE')
    command_counter: int = peewee.IntegerField(default=1)
    
    def __str__(self) -> str:
        return self.content