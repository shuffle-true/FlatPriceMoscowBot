import pandas as pd
import numpy as np
import re
from geopy import distance

class Preprocessing:
    def __init__(self):
        pass

    def __read_csv(self):
        """
        Читаем необработанный фрейм с квартирами
        """

        self.__df = pd.read_csv('DataFrameFlat.csv')

        return self.__df

    def __append_square_flat(self, df):
        """
        Исправляем площадь
        """

        self.__square_flat = []
        self.__name_flat_list = list(df['flat_name'])

        for i in range(len(self.__name_flat_list)):
            self.__square_flat.append(self.__name_flat_list[i].split(', ')[1].replace('м²', '').strip())

        self.__df['square'] = self.__square_flat

        return self.__df, self.__name_flat_list

    def __append_count_room(self, df, name_flat_list):
        """
        Ищем кол-во комнат в названии квартиры
        """

        self.__count_room = []

        for i in range(len(self.__name_flat_list)):
            self.__room_list = list(name_flat_list[i])

            if self.__room_list[0].isdigit():
                self.__count_room.append(self.__room_list[0])

            elif self.__room_list[0] == 'С' or self.__room_list[0] == 'А':
                self.__count_room.append('0')

            else:
                self.__count_room.append('7')

        self.__df['count_room'] = self.__count_room

        return df



    def __append_type_housing(self, name_flat_list):
        """
        Добавляем тип квартиры
        """

        self.__name_flat_list = name_flat_list
        self.__type_list = []
        self.__type_housing = []

        for i in range(len(self.__name_flat_list)):
            self.__type_list.append(self.__name_flat_list[i].split(',')[0].split('.'))

        for j in range(len(self.__name_flat_list)):
            try:
                self.__type_housing.append(self.__type_list[j][1].strip().capitalize())

            except IndexError:
                if list(self.__type_list[j][0])[0] == 'С':
                    self.__type_housing.append('Студия')

                else:
                    self.__type_housing.append('Квартира')

        self.__df['type_of_housing'] = self.__type_housing

        return self.__df

    def __append_district(self, df):
        """
        Чистим от мусора колонку "район"
        """

        self.__df = df
        self.__district_list = []
        self.__name_district_list = list(self.__df['district'])

        for i in range(len(self.__name_district_list)):
            try:
                self.__district_list.append(self.__name_district_list[i].split('р-н ')[1])

            except IndexError:
                self.__district_list.append(self.__name_district_list[i].split('р-н ')[0].split(' ')[0])

        self.__df['district'] = self.__district_list

        return self.__df


    def __join_year_house(self, df):
        """
        Добавляем год постройки дома в одну колонку
        """

        self.__df = df
        self.__year_house = list(self.__df['Построен'])
        self.__house_year = list(self.__df['Год постройки'])

        for i in range(self.__df['Построен'].shape[0]):
            if self.__year_house[i] == self.__house_year[i]:
                pass

            else:
                self.__year_house[i] = self.__house_year[i]

        self.__df['built_house'] = self.__year_house

        return self.__df

    def __separation_bathroom(self, df):
        """
        Обрабатываем колонку "санузел"
        """

        self.__df = df
        self.__bathroom_list = list(self.__df['Санузел'])
        self.__separation_bathroom = []

        for i in range(len(self.__bathroom_list)):
            try:
                digit_list = re.findall(r'\d+', self.__bathroom_list[i])

                if len(digit_list) == 2:
                    self.__separation_bathroom.append(int(digit_list[0]) + int(digit_list[1]))

                else:
                    self.__separation_bathroom.append(int(digit_list[0]))

            except TypeError:
                self.__separation_bathroom.append(1)

        self.__df['bathroom'] = self.__separation_bathroom

        return self.__df

    def __summ_lift(self, df):
        """
        Считаем сумму лифтов
        """

        self.__df = df
        self.__lift_list = list(self.__df['Лифты'])
        self.__summ_lift = []

        for i in range(len(self.__lift_list)):

            try:
                self.__digit_list = re.findall(r'\d+', self.__lift_list[i])

                if len(self.__digit_list) == 2:
                    self.__summ_lift.append(int(self.__digit_list[0]) + int(self.__digit_list[1]))

                if len(self.__digit_list) == 1:
                    self.__summ_lift.append(int(self.__digit_list[0]))

                if len(self.__digit_list) == 0:
                    self.__summ_lift.append(int(1))

            except TypeError:
                self.__summ_lift.append(int(1))

        self.__df['elevators'] = self.__summ_lift

        return self.__df


    def __one_floor(self, df):
        """
        Делаем только текущий этаж
        """

        self.__df = df
        self.__df['Этаж'] = self.__df['Этаж'].fillna('5')
        self.__floor_list = list(self.__df['Этаж'])
        self.__one_floor_list = []

        for i in range(len(self.__floor_list)):
            self.__one_floor_list.append(re.findall(r'\d+', self.__floor_list[i])[0])

        self.__df['floor'] = self.__one_floor_list

        return self.__df

    def __sum_balkon(self, df):
        """
        Считаем суммы балконов
        """

        self.__df = df
        self.__balkon_list = list(self.__df['Балкон/лоджия'])
        self.__sum_balkon = []

        for i in range(len(self.__balkon_list)):
            try:
                self.__digit_list = re.findall(r'\d+', self.__balkon_list[i])

                if len(self.__digit_list) == 2:
                    self.__sum_balkon.append(int(self.__digit_list[0]) + int(self.__digit_list[1]))

                else:
                    self.__sum_balkon.append(int(self.__digit_list[0]))

            except TypeError:
                self.__sum_balkon.append(int(0))

        self.__df['balcony'] = self.__sum_balkon

        return self.__df

    def __house_list_clean(self, df):
        """
        Чистим колонку номер дома от мусора
        """

        self.__df = df
        self.__df['house'].fillna('10', inplace=True)
        self.__house_list = list(self.__df['house'])
        self.__house_list_ready = []

        for i in range(self.__df['house'].shape[0]):
            self.__str_house_list = list(self.__house_list[i])

            for j in range(len(self.__str_house_list)-1):

                if self.__str_house_list[j] == 'к' or self.__str_house_list[j] == 'с' or self.__str_house_list[j] == 'К' or self.__str_house_list[j] == 'С':
                    self.__str_house_list.pop(j)

                    for k in range(j, len(self.__str_house_list)):
                        self.__str_house_list.pop(j)
                    break

            self.__house_list_ready.append(''.join(self.__str_house_list))

        self.__df['house'] = self.__house_list_ready

        return self.__df

    def __clear_obj_not_coord(self, df):
        """
        Удаляем объекты без координат
        """

        self.__df = df
        self.__df['coord'].replace('', np.nan, inplace=True)
        self.__df.dropna(subset=['coord'], inplace=True)

        return self.__df

    def __fillna(self, df):
        """
        Заполняем пропуски
        """

        self.__df = df
        self.__df['built_house'] = self.__df['built_house'].fillna(self.__df['built_house'].med())
        self.__df['repair_flat'] = self.__df['Ремонт'].fillna('Косметический')
        self.__df['view_outside'] = self.__df['Вид из окон'].fillna('На улицу')
        self.__df['type_house'] = self.__df['Тип дома'].fillna('Монолитный')
        self.__df['parking'] = self.__df['Парковка'].fillna('Открытая')
        self.__df['metro_time'] = self.__df['metro_time'].fillna(self.__df['metro_time'].med())
        self.__df['Залог'] = np.where((self.__df['Залог'] != 0), 1, self.__df['Залог'])

        return self.__df

    def __append_info_district(self, df):
        """
        Добавляем информацию о районе
        """

        self.__df = df
        self.__df_1 = pd.read_csv('DISTRICT.csv')
        self.__df_1 = self.__df_1[['Название района', 'Музеи', 'Салоны красоты косметических услуг',
        'Рестораны / кафе быстрого питания','Продовольственные магазины', 'Городские парки развлечений, аттракционов','Аптеки по продаже лекарств',
        'Маммологические центры, больницы, клиники, поликлиники','Фитнес-клубы, центры, залы']]
        self.__df = self.__df.merge(self.__df_1, left_on="district", right_on="Название района")

        return self.__df

    def __dist_kreml(self, df):
        """
        Считаем расстояние до Кремля
        """
        self.__df = df
        self.__kreml_dist_list = []
        self.__kreml = (55.752004, 37.617734)

        for i in range(self.__df.shape[0]):
            self.__lat = self.__df['lat'][i]

            self.__lon = self.__df['lon'][i]

            self.__kreml_dist_list.append(float(distance.distance((self.__lat, self.__lon), self.__kreml).km))

        self.__df['dist_kreml'] = self.__kreml_dist_list

        return self.__df

    def __circle(self, df):
        """
        Смотрим внутри какого кольца находится квартира
        """
        self.__df = df
        self.__circle = []
        self.__df['lat'] = self.__df['lat'].apply(lambda x: float(x))

        for i in range(self.__df['lat'].shape[0]):

            if self.__df['lat'][i]<=55.7888532 and self.__df['lat'][i] >=55.7014943:

                if self.__df['dist_kreml'][i] < 1.5:
                    self.__circle.append('Бульварное')

                elif self.__df['dist_kreml'][i] >= 1.5 and self.__df['dist_kreml'][i] < 3:
                    self.__circle.append('Садовое')

                elif self.__df['dist_kreml'][i] >= 3 and self.__df['dist_kreml'][i] < 6:
                    self.__circle.append('3 Транспортное')

                elif self.__df['dist_kreml'][i] >= 6 and self.__df['dist_kreml'][i] < 14:
                    self.__circle.append('В пределах МКАД')

                else:
                    self.__circle.append('За МКАД')

            else:
                if self.__df['dist_kreml'][i] < 1.5:
                    self.__circle.append('Бульварное')

                elif self.__df['dist_kreml'][i] >= 1.5 and self.__df['dist_kreml'][i] < 3:
                    self.__circle.append('Садовое')

                elif self.__df['dist_kreml'][i] >= 3 and self.__df['dist_kreml'][i] < 6:
                    self.__circle.append('3 Транспортное')

                elif self.__df['dist_kreml'][i] >= 6 and self.__df['dist_kreml'][i] < 17:
                    self.__circle.append('В пределах МКАД')

                else:
                    self.__circle.append('За МКАД')

        self.__df['circle'] = self.__circle

        return self.__df

    def __get_dummy(self, df):
        """
        One-Hot_Encoding
        """

        self.__df = df
        self.__df_dummy = pd.get_dummies(self.__df[['district','type_of_housing','repair_flat','view_outside','type_house','parking', 'circle']])
        self.__df = pd.concat([self.__df, self.__df_dummy], axis = 1)

        return self.__df

    def __data_df(self, df):
        """
        Отделяем цену от всего фрейма
        """

        self.__df = df
        self.__df['price']= self.__df['price'].apply(lambda x: x.replace(' ', ''))
        self.__data = self.__df['price']

        return self.__data

    def __standart_after_preprocessing(self, df):
        """
        Удаляем лишние колонки
        """

        self.__df = df

        self.__df = self.__df.drop(['price','city','okrug','district','street', 'house','Тип жилья',
                 'Площадь комнат+ обозначение смежных комнат- обозначение изолированных комнат',
                 'Высота потолков','Санузел','Ремонт','bathroom', 'Душевая кабина', 'Стиральная машина', 'Посудомоечная машина', 'Холодильник',
                      'Телевизор', 'Кондиционер', 'Интернет', 'Ванна',
                 'Вид из окон','Тип дома','Общая','Жилая','Кухня','Этаж',
                'Парковка','Аварийность','Балкон/лоджия','Ванная комната','Газоснабжение',
                'Год постройки','Отопление','Планировка','Подъезды','Построен','Строительная серия',
                'Тип перекрытий',
                'Лифты','Мусоропровод','type_of_housing','repair_flat','view_outside','type_house',
                'parking','circle', 'flat_name', 'coord', 'lat', 'lon', 'Название района', 'Количество спальных мест'], axis=1)

        return self.__df

    def run_preprocessing_script(self):
        """
        Запуск скрипта
        """

        self.__df = self.__read_csv()
        self.__df = self.__append_square_flat(self.__df)[0]
        self.__df = self.__append_count_room(self.__df, self.__append_square_flat(self.__df)[1])
        self.__df = self.__append_type_housing(self.__df, self.__append_square_flat(self.__df)[1])
        self.__df = self.__append_district(self.__df)
        self.__df = self.__join_year_house(self.__df)
        self.__df = self.__separation_bathroom(self.__df)
        self.__df = self.__summ_lift(self.__df)
        self.__df = self.__one_floor(self.__df)
        self.__df = self.__sum_balkon(self.__df)
        self.__df = self.__house_list_clean(self.__df)
        self.__df = self.__clear_obj_not_coord(self.__df)
        self.__df = self.__fillna(self.__df)
        self.__df = self.__append_info_district(self.__df)
        self.__df = self.__dist_kreml(self.__df)
        self.__df = self.__circle(self.__df)
        self.__df = self.__get_dummy(self.__df)
        self.__data = self.__data_df(self.__df)
        self.__df = self.__standart_after_preprocessing(self.__df)
        self.__df.to_excel('DataFrame_after_preprocessing.xlsx', index = False)
        self.__data.to_excel('Value_after_preprocessing.xlsx', index = False)
        self.__df.to_csv('DataFrame_after_preprocessing.csv', index = False)
        self.__data.to_csv('Value_after_preprocessing.csv', index = False)

    
