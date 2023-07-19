import peewee
from datetime import datetime

from database.models.base import DefaultDatabaseModel
from database.models import DiscordUser


class Command(DefaultDatabaseModel):
    content: str = peewee.TextField(null=False)
    created: int = peewee.DateTimeField(default=datetime.now)
    updated: int = peewee.DateTimeField(default=datetime.now, null=True)
    user: int = peewee.ForeignKeyField(DiscordUser, 
                                       backref='commands',
                                       on_delete='CASCADE')
    
    def __str__(self) -> str:
        return self.content