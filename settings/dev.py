from dotenv import load_dotenv
import os

load_dotenv()

CHANNEL_ACCESS_TOKEN = os.getenv("CHANNEL_ACCESS_TOKEN")
CHANNEL_SECRET = os.getenv("CHANNEL_SECRET")
ROOM_TRANSACTION_URL = os.getenv("ROOM_TRANSACTION_URL")