import peewee
from datetime import datetime

from database.models.base import DefaultDatabaseModel


class DiscordUser(DefaultDatabaseModel):
    username: str = peewee.CharField(max_length=50, 
                                     null=False,
                                     unique=True)
    guildname: str = peewee.CharField(max_length=50)
    created_at: int = peewee.DateTimeField(default=datetime.now())
    joined_at: int = peewee.DateTimeField(default=datetime.now())
    is_bot: bool = peewee.BooleanField(default=False, null=False)
    is_admin: peewee.BooleanField = peewee.BooleanField(default=False, null = False)

    @classmethod
    def create_new_user(cls, username: peewee.CharField, 
                             guildname: peewee.CharField,
                             created_at: peewee.DateTimeField,
                             joined_at: peewee.DateTimeField):
        return cls.create(username=username,
                          guildname=guildname,
                          created_at=created_at)
    
    @classmethod
    def create_new_admin(cls, username: peewee.CharField, 
                              guildname: peewee.CharField,
                              created_at: peewee.DateTimeField,
                              admin: peewee.BooleanField = True):
        return cls.create(username=username,
                          guildname=guildname,
                          created_at=created_at,
                          is_admin=admin)
    
    @classmethod
    def update_user_to_admin(cls, username: peewee.CharField, 
                                  admin: peewee.BooleanField = True):
        cls.update(is_admin=admin).where(cls.username==username).execute()
        return cls.get(username==cls.username)

    def __str__(self) -> str:
        return self.username