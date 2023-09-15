import os

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
# FIXME: does not work as an environment variable
CHANNEL_ID = 1125323466921476118
GUILD = os.getenv("DISCORD_GUILD")
DATABASE_NAME = os.getenv("DATABASE_NAME")
DATABASE_NAME_TEST = os.getenv("DATABASE_NAME_TEST")
USER_NAME = os.getenv("USER_NAME")
PASSWORD = os.getenv("PASSWORD")
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
APIKEY_JSON = os.getenv("APIKEY_JSON")
APIKEY_AI = os.getenv("APIKEY_AI")
