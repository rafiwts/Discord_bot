import peewee
import pytest
from datetime import datetime

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


@pytest.fixture(scope="class")
def session():
    postgres_db.bind(MODELS)
    postgres_db.drop_tables(MODELS)
    postgres_db.create_tables(MODELS)
    try:
        yield postgres_db
    except peewee.DatabaseError as err:
        print("Database error: ", err)
    postgres_db.close()
    