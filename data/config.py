import os

from dotenv import load_dotenv
from data.all_config import TOKEN

load_dotenv()

BOT_TOKEN = TOKEN
admins = [
    314715042
]

ip = os.getenv("ip")

aiogram_redis = {
    'host': ip,
}

redis = {
    'address': (ip, 6379),
    'encoding': 'utf8'
}