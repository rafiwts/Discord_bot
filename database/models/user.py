import peewee
import discord
from datetime import datetime

from database.models.base import DefaultDatabaseModel


class DiscordUser(DefaultDatabaseModel):
    discord_id = peewee.BigIntegerField(unique=True)
    username: str = peewee.CharField(max_length=50, null=False, unique=True)
    guildname: str = peewee.CharField(max_length=50, null=False)
    created_at: int = peewee.DateTimeField(default=datetime.now())
    joined_at: int = peewee.DateTimeField(default=datetime.now())
    is_bot: bool = peewee.BooleanField(default=False, null=False)
    is_admin: peewee.BooleanField = peewee.BooleanField(default=False, null=False)
    banned: peewee.BooleanField = peewee.BooleanField(default=False, null=False)

    @classmethod
    def create_new_user(cls, discord_user: discord.Member, guildname: peewee.CharField):
        return cls.create(
            discord_id=discord_user.id,
            username=discord_user.name,
            guildname=guildname,
            created_at=discord_user.created_at,
        )

    @classmethod
    def get_or_create_user(cls, sender: discord.Member):
        discord_user = cls.get_or_none(discord_id=sender.id)
        if discord_user is None:
            discord_user = cls.create(
                discord_id=sender.id,
                username=sender.name,
                guildname=sender.guild,
                created_at=sender.created_at,
                joined_at=sender.joined_at,
            )

            discord_user.save()

        return discord_user

    @classmethod
    def create_new_admin(
        cls,
        bot_owner: discord.Member,
        guildname: peewee.CharField,
        admin: peewee.BooleanField = True,
    ):
        return cls.create(
            discord_id=bot_owner.id,
            username=bot_owner.name,
            guildname=guildname,
            created_at=bot_owner.created_at,
            is_admin=admin,
        )

    @classmethod
    def update_user_to_admin(
        cls, discord_id: peewee.CharField, admin: peewee.BooleanField = True
    ):
        cls.update(is_admin=admin).where(cls.discord_id == discord_id).execute()
        return cls.get(discord_id == cls.discord_id)

    @classmethod
    def update_user_data(
        cls,
        discord_user: discord.Member,
        guild: discord.Guild,
        updated_user: discord.Member = None,
        banned: bool = None,
    ):
        if banned is None:
            cls.update(username=updated_user.name, guildname=guild).where(
                cls.discord_id == discord_user.id
            ).execute()
        else:
            cls.update(banned=banned).where(cls.discord_id == discord_user.id).execute()

    def __str__(self) -> str:
        return self.username
