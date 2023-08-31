import peewee
from discord.ext import commands

from database.models.base import DefaultDatabaseModel
from database.models import DiscordUser


class BotUser(DefaultDatabaseModel):
    discord_id: peewee.BigIntegerField = peewee.BigIntegerField(unique=True)
    botname: peewee.CharField = peewee.CharField(max_length=50, null=False, unique=True)
    command_prefix: peewee.CharField = peewee.CharField(max_length=50, null=False)
    owner: peewee.ForeignKeyField = peewee.ForeignKeyField(
        DiscordUser, backref="owner", on_delete="CASCADE"
    )

    @classmethod
    def create_new_bot(cls, bot: commands.Bot, owner_id: peewee.ForeignKeyField):
        return cls.create(
            discord_id=bot.application_id,
            botname=bot.user,
            command_prefix=bot.command_prefix,
            owner_id=owner_id,
        )

    @classmethod
    def check_user_or_bot(cls, discord_id: peewee.BigIntegerField):
        try:
            return DiscordUser.get(discord_id=discord_id)
        except DiscordUser.DoesNotExist:
            return cls.get(discord_id=discord_id)

    def __str__(self) -> str:
        return self.botname
