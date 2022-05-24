from selenium.webdriver.chrome.service import Service
import os

TOKEN = r"{0}".format(str(input("Enter bot TOKEN below ->\n")))

find_driver = r"{0}".format(os.path.abspath("handlers/users/parser/chromedriver.exe"))
Andrew_PATH_driver = Service(find_driver)




































































columns = ['price', 'Комиссия', 'count_room', 'built_house', 'balcony',
       'Наличие мебели', 'Музеи', 'Салоны красоты косметических услуг',
       'Рестораны / кафе быстрого питания', 'Продовольственные магазины',
       'Городские парки развлечений, аттракционов',
       'Аптеки по продаже лекарств',
       'Маммологические центры, больницы, клиники, поликлиники',
       'Фитнес-клубы, центры, залы', 'repair_flat_Дизайнерский',
       'repair_flat_Евроремонт', 'repair_flat_Косметический',
       'view_outside_Во двор', 'view_outside_На улицу',
       'view_outside_На улицу и двор', 'type_house_Блочный',
       'type_house_Кирпичный', 'type_house_Монолитно кирпичный',
       'type_house_Монолитный', 'type_house_Панельный', 'parking_Наземная',
       'parking_Открытая', 'parking_Подземная', 'circle_3 Транспортное',
       'circle_Бульварное', 'circle_В пределах МКАД', 'circle_За МКАД',
       'circle_Садовое', 'budget', 'coef_bern', 'coef_migrant',
       'coef_people_prirost', 'coef_children', 'coef_year_people',
       'coef_plotnost_people', 'coef_bacalavr_degree', 'coef_russian_people',
       'coef_green_zone', 'coef_life_house', 'coef_happy_house',
       'coef_ecology', 'square_log', 'metro_time_log', 'floor_log',
       'azdist_log', 'mpa']

columns_1 = ['Название района', 'Музеи', 'Салоны красоты косметических услуг',
                             'Рестораны / кафе быстрого питания', 'Продовольственные магазины',
                             'Городские парки развлечений, аттракционов', 'Аптеки по продаже лекарств',
                             'Маммологические центры, больницы, клиники, поликлиники', 'Фитнес-клубы, центры, залы']

columns_1_0 = ['Музеи', 'Салоны красоты косметических услуг',
                             'Рестораны / кафе быстрого питания', 'Продовольственные магазины',
                             'Городские парки развлечений, аттракционов', 'Аптеки по продаже лекарств',
                             'Маммологические центры, больницы, клиники, поликлиники', 'Фитнес-клубы, центры, залы']

columns_2 = ['district', 'budget', 'coef_bern', 'coef_migrant',
       'coef_people_prirost', 'coef_children', 'coef_year_people',
       'coef_plotnost_people', 'coef_bacalavr_degree', 'coef_russian_people',
       'coef_green_zone', 'coef_life_house', 'coef_happy_house',
       'coef_ecology']

columns_2_0 = ['budget', 'coef_bern', 'coef_migrant',
       'coef_people_prirost', 'coef_children', 'coef_year_people',
       'coef_plotnost_people', 'coef_bacalavr_degree', 'coef_russian_people',
       'coef_green_zone', 'coef_life_house', 'coef_happy_house',
       'coef_ecology']