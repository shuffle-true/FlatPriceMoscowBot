import pandas as pd
import numpy as np
import re
from geopy import distance

def read_csv():
    df = pd.read_csv('DataFrameFlat.csv')
    return df

def append_square_flat(df):
    square_flat = []
    name_flat_list = []
    name_flat_list = list(df['flat_name'])
    for i in range(len(name_flat_list)):
        square_flat.append(name_flat_list[i].split(', ')[1].replace('м²', '').strip())
    df['square'] = square_flat
    return df, name_flat_list

def append_count_room(df, name_flat_list):
    count_room = []  # сюда будет записывать площадь
    for i in range(len(name_flat_list)):
        room_list = []
        room_list = list(name_flat_list[i])
        if room_list[0].isdigit():
            count_room.append(room_list[0])
        elif room_list[0] == 'С' or room_list[0] == 'А':
            count_room.append('0')
        else: 
            count_room.append('7')
    df['count_room'] = count_room
    return df



def append_type_housing(df, name_flat_list):
    type_list = []
    type_housing = []
    for i in range(len(name_flat_list)):
        type_list.append(name_flat_list[i].split(',')[0].split('.'))
    for j in range(len(name_flat_list)):
        try:
            type_housing.append(type_list[j][1].strip().capitalize())
        except IndexError:
            if list(type_list[j][0])[0] == 'С':
                type_housing.append('Студия')
            else:
                type_housing.append('Квартира')
    df['type_of_housing'] = type_housing
    return df

def append_district(df):
    name_district_list = []
    district_list = []
    name_district_list = list(df['district'])
    for i in range(len(name_district_list)):
        try:
            district_list.append(name_district_list[i].split('р-н ')[1])
        except IndexError:
            district_list.append(name_district_list[i].split('р-н ')[0].split(' ')[0])  
    
    df['district'] = district_list
    return df


def join_year_house(df):
    year_house = list(df['Построен'])
    house_year = list(df['Год постройки'])
    for i in range(df['Построен'].shape[0]):
        if year_house[i] == house_year[i]:
            pass
        else:
            year_house[i] == house_year[i]
    df['built_house'] = year_house
    return df

def separation_bathroom(df):
    bathroom_list = list(df['Санузел'])
    separation_bathroom = []

    for i in range(len(bathroom_list)):
        try:
            digit_list = re.findall(r'\d+', bathroom_list[i])
            if len(digit_list) == 2:
                separation_bathroom.append(int(digit_list[0]) + int(digit_list[1]))
            else:
                separation_bathroom.append(int(digit_list[0]))  
        except TypeError:
            separation_bathroom.append(1)
    df['bathroom'] = separation_bathroom
    return df

def summ_lift(df):
    lift_list = list(df['Лифты'])
    summ_lift = []
    for i in range(len(lift_list)):
        try:
            digit_list = re.findall(r'\d+', lift_list[i])
            if len(digit_list) == 2:
                summ_lift.append(int(digit_list[0]) + int(digit_list[1]))
            if len(digit_list) == 1:
                summ_lift.append(int(digit_list[0]))
            if len(digit_list) == 0:
                summ_lift.append(int(1))      
        except TypeError:
            summ_lift.append(int(1))
    df['elevators'] = summ_lift
    return df


def one_floor(df):
    df['Этаж'] = df['Этаж'].fillna('5')
    floor_list = list(df['Этаж'])
    one_floor_list = []
    for i in range(len(floor_list)):
        one_floor_list.append(re.findall(r'\d+', floor_list[i])[0])
    df['floor'] = one_floor_list
    return df

def sum_balkon(df):
    balkon_list = list(df['Балкон/лоджия'])
    sum_balkon = []
    for i in range(len(balkon_list)):
        try:
            digit_list = re.findall(r'\d+', balkon_list[i])
            if len(digit_list) == 2:
                sum_balkon.append(int(digit_list[0]) + int(digit_list[1]))
            else:
                sum_balkon.append(int(digit_list[0]))
        except TypeError:
            sum_balkon.append(int(0))
    df['balcony'] = sum_balkon
    return df

def house_list_clean(df):
    df['house'].fillna('10', inplace=True)
    house_list = list(df['house'])
    house_list_ready = []
    for i in range(df['house'].shape[0]):
        str_house_list = list(house_list[i])
        for j in range(len(str_house_list)-1):
            if str_house_list[j] == 'к' or str_house_list[j] == 'с' or str_house_list[j] == 'К' or str_house_list[j] == 'С':
                str_house_list.pop(j)
                for k in range(j, len(str_house_list)):
                    str_house_list.pop(j)
                break
        house_list_ready.append(''.join(str_house_list))
    df['house'] = house_list_ready
    return df

def clear_obj_not_coord(df):
    df['coord'].replace('', np.nan, inplace=True)
    df.dropna(subset=['coord'], inplace=True)
    return df

def fillna(df):
    df['built_house'] = df['built_house'].fillna('2000')
    df['repair_flat'] = df['Ремонт'].fillna('Косметический')
    df['view_outside'] = df['Вид из окон'].fillna('На улицу')
    df['type_house'] = df['Тип дома'].fillna('Монолитный')
    df['parking'] = df['Парковка'].fillna('Открытая')
    df['Залог'] = np.where((df['Залог'] != 0), 1, df['Залог'])
    return df

def append_info_district(df):
    df_1 = pd.read_csv('DISTRICT.csv')
    df_1 = df_1[['Название района', 'Музеи', 'Салоны красоты косметических услуг',
    'Рестораны / кафе быстрого питания','Продовольственные магазины', 'Городские парки развлечений, аттракционов','Аптеки по продаже лекарств',
    'Маммологические центры, больницы, клиники, поликлиники','Фитнес-клубы, центры, залы']]
    df = df.merge(df_1, left_on="district", right_on="Название района")
    return df

def dist_kreml(df):
    kreml_dist_list = []
    kreml = (55.752004, 37.617734)
    for i in range(df.shape[0]):
        lat = df['lat'][i]
        lon = df['lon'][i]
        kreml_dist_list.append(float(distance.distance((lat, lon), kreml).km))
    df['dist_kreml'] = kreml_dist_list
    return df

def circle(df):
    circle = []
    df['lat'] = df['lat'].apply(lambda x: float(x))
    for i in range(df['lat'].shape[0]):
        if df['lat'][i]<=55.7888532 and df['lat'][i] >=55.7014943:
            if df['dist_kreml'][i] < 1.5:
                circle.append('Бульварное')
            elif df['dist_kreml'][i] >= 1.5 and df['dist_kreml'][i] < 3:
                circle.append('Садовое')
            elif df['dist_kreml'][i] >= 3 and df['dist_kreml'][i] < 6:
                circle.append('3 Транспортное')
            elif df['dist_kreml'][i] >= 6 and df['dist_kreml'][i] < 14:
                circle.append('В пределах МКАД')
            else:
                circle.append('За МКАД')
        else:
            if df['dist_kreml'][i] < 1.5:
                circle.append('Бульварное')
            elif df['dist_kreml'][i] >= 1.5 and df['dist_kreml'][i] < 3:
                circle.append('Садовое')
            elif df['dist_kreml'][i] >= 3 and df['dist_kreml'][i] < 6:
                circle.append('3 Транспортное')
            elif df['dist_kreml'][i] >= 6 and df['dist_kreml'][i] < 17:
                circle.append('В пределах МКАД')
            else:
                circle.append('За МКАД')
    df['circle'] = circle
    return df

def get_dummy(df):
    df_dummy = pd.get_dummies(df[['district','type_of_housing','repair_flat','view_outside','type_house','parking', 'circle']])
    df = pd.concat([df, df_dummy], axis = 1)
    return df

def data_df(df):
    df['price']= df['price'].apply(lambda x: x.replace(' ', ''))
    data = df['price']
    return data

def standart_after_preprocessing(df):
    df = df.drop(['price','city','okrug','district','street', 'house','Тип жилья',
             'Площадь комнат+ обозначение смежных комнат- обозначение изолированных комнат',
             'Высота потолков','Санузел','Ремонт','bathroom', 'Душевая кабина', 'Стиральная машина', 'Посудомоечная машина', 'Холодильник',
                  'Телевизор', 'Кондиционер', 'Интернет', 'Ванна',
             'Вид из окон','Тип дома','Общая','Жилая','Кухня','Этаж',
            'Парковка','Аварийность','Балкон/лоджия','Ванная комната','Газоснабжение',
            'Год постройки','Отопление','Планировка','Подъезды','Построен','Строительная серия',
            'Тип перекрытий',
            'Лифты','Мусоропровод','type_of_housing','repair_flat','view_outside','type_house',
            'parking','circle', 'flat_name', 'coord', 'lat', 'lon', 'Название района', 'Количество спальных мест'], axis=1)
    return df

def run_preprocessing_script():
    df = read_csv()
    df = append_square_flat(df)[0]
    df = append_count_room(df, append_square_flat(df)[1])
    df = append_type_housing(df, append_square_flat(df)[1])
    df = append_district(df)
    df = join_year_house(df)
    df = separation_bathroom(df)
    df = summ_lift(df)
    df = one_floor(df)
    df = sum_balkon(df)
    df = house_list_clean(df)
    df = clear_obj_not_coord(df)
    df = fillna(df)
    df = append_info_district(df)
    df = dist_kreml(df)
    df = circle(df)
    df = get_dummy(df)
    data = data_df(df)
    df = standart_after_preprocessing(df)
    df.to_excel('DataFrame_after_preprocessing.xlsx', index = False)
    data.to_excel('Value_after_preprocessing.xlsx', index = False)    
    df.to_csv('DataFrame_after_preprocessing.csv', index = False)
    data.to_csv('Value_after_preprocessing.csv', index = False)

    
