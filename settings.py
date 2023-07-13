import os
import pathlib
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')
#FIXME: does not work as an environment variable
CHANNEL_ID = 1125323466921476118 
GUILD = os.getenv('DISCORD_GUILD')
BASE_DIR = pathlib.Path(__file__).parent