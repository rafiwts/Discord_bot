import peewee
import pytest
import discord
from datetime import datetime
from unittest.mock import Mock

import settings
from database.models import (
            DiscordUser,
            Event,
            Reaction,
            Message,
            BotUser,
            Command
)

postgres_db = peewee.PostgresqlDatabase(settings.DATABASE_NAME_TEST,
                                        user=settings.USER_NAME,
                                        password=settings.PASSWORD,
                                        host=settings.HOST,
                                        port=settings.PORT)


MODELS = [DiscordUser, Event, Reaction, Message, BotUser, Command]


@pytest.fixture
def session():
    postgres_db.bind(MODELS)
    postgres_db.drop_tables(MODELS)
    postgres_db.create_tables(MODELS)
    try:
        yield postgres_db
    except peewee.DatabaseError as err:
        print("Database error: ", err)
    postgres_db.close()


@pytest.fixture
def mock_time():
    get_mock_time = datetime.now()
    return get_mock_time


@pytest.fixture
def mock_discord_user(mock_time):
    return DiscordUser.create(
        id=2,
        discord_id=1111,
        username="Rafiwts",
        guildname="Gildia",
        created_at=mock_time,
        joined_at=mock_time
    )


@pytest.fixture
def mock_discord_users(mock_time):   
    DiscordUser.create(
        id=1,
        discord_id=1111,
        username="User one",
        guildname="Gildia",
        created_at=mock_time,
        joined_at=mock_time
    )

    DiscordUser.create(
        id=2,
        discord_id=2222,
        username="User two",
        guildname="Gildia",
        created_at=mock_time,
        joined_at=mock_time
    )

    DiscordUser.create(
        id=3,
        discord_id=3333,
        username="User three",
        guildname="Gildia",
        created_at=mock_time,
        joined_at=mock_time
    )

    DiscordUser.create(
        id=4,
        discord_id=4444,
        username="User four",
        guildname="Gildia",
        created_at=mock_time,
        joined_at=mock_time
    )


@pytest.fixture
def mock_discord_user_and_message(mock_time):
    DiscordUser.create(
        id=1,
        discord_id=1111,
        username="Username",
        guildname="Guildname",
        create_at=mock_time,
        joined_at=mock_time
    )

    Message.create(
        discord_id=1010,
        content="I wrote a message",
        created_at=mock_time,
        user=1
    )