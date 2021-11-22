import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = "2103971375:AAFWfc-AYxS13sCFEqZYhZVtsDBS6XByXSc"
admins = [
    469824120,314715042

]

ip = os.getenv("ip")

aiogram_redis = {
    'host': ip,
}

redis = {
    'address': (ip, 6379),
    'encoding': 'utf8'
}