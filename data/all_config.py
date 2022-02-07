import pandas as pd
from selenium.webdriver.chrome.service import Service
TOKEN = r"2145614320:AAEEkcgJRryvRVPhbVUdOWPAvM7iZwAV718"
Andrew_PATH_driver = Service(r"C:\Users\Andrew\Desktop\tg-bot\handlers\users\parser\chromedriver.exe")
df = pd.read_csv("DataFrame_after_preprocessing.csv")
columns = list(df.columns)

columns_1 = ['Название района', 'Музеи', 'Салоны красоты косметических услуг',
                             'Рестораны / кафе быстрого питания', 'Продовольственные магазины',
                             'Городские парки развлечений, аттракционов', 'Аптеки по продаже лекарств',
                             'Маммологические центры, больницы, клиники, поликлиники', 'Фитнес-клубы, центры, залы']

columns_1_0 = ['Музеи', 'Салоны красоты косметических услуг',
                             'Рестораны / кафе быстрого питания', 'Продовольственные магазины',
                             'Городские парки развлечений, аттракционов', 'Аптеки по продаже лекарств',
                             'Маммологические центры, больницы, клиники, поликлиники', 'Фитнес-клубы, центры, залы']