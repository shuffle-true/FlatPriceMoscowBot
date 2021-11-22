import os

from dotenv import load_dotenv
from data.TOKEN_config import TOKEN

load_dotenv()

BOT_TOKEN = TOKEN
admins = [
    314715042, 469824120
]

ip = os.getenv("ip")

aiogram_redis = {
    'host': ip,
}

redis = {
    'address': (ip, 6379),
    'encoding': 'utf8'
}