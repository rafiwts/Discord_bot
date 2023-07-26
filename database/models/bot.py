import peewee

from database.models.base import DefaultDatabaseModel
from database.models import DiscordUser


class BotUser(DefaultDatabaseModel):
    botname: peewee.CharField = peewee.CharField(max_length=50, 
                                                 null=False,
                                                 unique=True)
    command_prefix: peewee.CharField = peewee.CharField(max_length=50)
    owner_id: peewee.ForeignKeyField = peewee.ForeignKeyField(DiscordUser,
                                                              backref='owner',
                                                              on_delete='CASCADE')

    def __str__(self) -> str:
        return self.botname