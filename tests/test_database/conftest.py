from datetime import datetime

import peewee
import pytest

import settings
from database.models import BotUser, Command, DiscordUser, Event, Message, Reaction

postgres_db = peewee.PostgresqlDatabase(
    settings.DATABASE_NAME_TEST,
    user=settings.USER_NAME,
    password=settings.PASSWORD,
    host=settings.HOST,
    port=settings.PORT,
)


MODELS = [DiscordUser, Event, Reaction, Message, BotUser, Command]


@pytest.fixture
def session():
    postgres_db.bind(MODELS)
    postgres_db.drop_tables(MODELS)
    postgres_db.create_tables(MODELS)
    try:
        yield postgres_db
        postgres_db.close()
    except peewee.DatabaseError as err:
        print("Database error: ", err)


@pytest.fixture
def mock_time():
    get_mock_time = datetime.now()
    return get_mock_time


@pytest.fixture
def mock_discord_user(mock_time):
    discord_user = DiscordUser.create(
        id=2,
        discord_id=1111,
        username="Rafiwts",
        guildname="Gildia",
        created_at=mock_time,
        joined_at=mock_time,
    )

    return discord_user


@pytest.fixture
def mock_discord_users(mock_time):
    DiscordUser.create(
        id=1,
        discord_id=1111,
        username="User one",
        guildname="Gildia",
        created_at=mock_time,
        joined_at=mock_time,
    )

    DiscordUser.create(
        id=2,
        discord_id=2222,
        username="User two",
        guildname="Gildia",
        created_at=mock_time,
        joined_at=mock_time,
    )

    DiscordUser.create(
        id=3,
        discord_id=3333,
        username="User three",
        guildname="Gildia",
        created_at=mock_time,
        joined_at=mock_time,
    )

    DiscordUser.create(
        id=4,
        discord_id=4444,
        username="User four",
        guildname="Gildia",
        created_at=mock_time,
        joined_at=mock_time,
    )


@pytest.fixture
def mock_discord_user_and_message(mock_time):
    DiscordUser.create(
        id=1,
        discord_id=1111,
        username="Username",
        guildname="Guildname",
        create_at=mock_time,
        joined_at=mock_time,
    )

    Message.create(discord_id=1010, content="message", created_at=mock_time, user=1)


@pytest.fixture
def mock_discord_messages(mock_time):
    Message.create(discord_id=1010, content="message1", created_at=mock_time, user=2)

    Message.create(discord_id=2020, content="message2", created_at=mock_time, user=3)

    Message.create(discord_id=3030, content="message3", created_at=mock_time, user=4)

    Message.create(discord_id=4040, content="message4", created_at=mock_time, user=1)


@pytest.fixture
def mock_discord_command(mock_discord_user):
    new_command = Command.create(content="!newcommand", user=mock_discord_user.id)

    return new_command


@pytest.fixture
def mock_bot_user(mock_discord_user):
    new_bot = BotUser.create(
        discord_id=1011, botname="Bot1", command_prefix="!", owner=mock_discord_user.id
    )

    return new_bot
