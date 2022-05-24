import os

from dotenv import load_dotenv
from data.all_config import TOKEN

load_dotenv()

BOT_TOKEN = TOKEN

print("Enter separated by spaces admin ID below ->")
admins = list(map(int, input().split()))

ip = os.getenv("ip")

aiogram_redis = {
    'host': ip,
}

redis = {
    'address': (ip, 6379),
    'encoding': 'utf8'
}