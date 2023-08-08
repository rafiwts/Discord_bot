import peewee
import discord
from datetime import datetime

from database.models.base import DefaultDatabaseModel
from database.models import DiscordUser, Message


class Reaction(DefaultDatabaseModel):
    user_from: int = peewee.ForeignKeyField(DiscordUser, 
                                            backref='senders',
                                            on_delete='CASCADE')
    user_to: int = peewee.ForeignKeyField(DiscordUser,
                                          backref='recipients',
                                          on_delete='CASCADE')
    message: int = peewee.ForeignKeyField(Message,
                                          backref='reactions',
                                          on_delete='CASCADE')
    added_at: int = peewee.DateTimeField(default=datetime.now())
    edited_at: int = peewee.DateTimeField(default=datetime.now())
   
    @classmethod
    def create_new_reaction(cls, user_from: peewee.ForeignKeyField,
                                 current_message: discord.Message):
        return cls.create(user_from=user_from,
                          user_to=current_message.user.id,
                          message=current_message.id)
    
    def __str__(self) -> str:
        return f'Reaction {self.id}'