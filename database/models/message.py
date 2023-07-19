import peewee
from datetime import datetime

from database.models.base import DefaultDatabaseModel
from database.models import DiscordUser


class Message(DefaultDatabaseModel):
    content: str = peewee.TextField(null=False)
    created_at: int = peewee.DateTimeField(default=datetime.now)
    edited_at: int = peewee.DateTimeField(default=datetime.now)
    user: int = peewee.ForeignKeyField(DiscordUser, 
                                       backref='messages',
                                       on_delete='CASCADE')
    
    def __str__(self) -> str:
        return f'Message {self.id}'