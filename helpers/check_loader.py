import os
from datetime import datetime

import pandas as pd
from enums.shop_name_enum import ShopName


class CheckLoader:
    def __init__(self, folder_path):
        self.folder_path = folder_path

    def load_check(self, shop_name):
        # Список для хранения данных из всех файлов
        dataframes = []
        # Чтение файлов из папки
        for filename in os.listdir(self.folder_path):
            if filename.endswith('.xlsx'):
                file_shop_name = filename.split('_')[0].title()
                if file_shop_name == shop_name:
                    print(f"Загружается файл {filename}")

                    # Загрузка данных из файла
                    filepath = os.path.join(self.folder_path, filename)
                    df = pd.read_excel(filepath, skiprows=10, header=None)

                    # Подготовка чека
                    df_prepared = self.check_prepare(df, shop_name)

                    # print('Сохраняем подготовленный датафрейм')
                    # df_prepared.to_excel(filename.split('.xlsx')[0] + '_prepared' + '.xlsx', index=False)
                    dataframes.append(df_prepared)
        return pd.concat(dataframes, ignore_index=True)  # Склейка датафрейма

    def file_to_df(self, file, shop_name):
        print(f"Загружается файл {file.name}")
        if file.name.endswith('.csv'):
            df = pd.read_csv(file, skiprows=10, header=None)
        elif file.name.endswith('.xlsx'):
            df = pd.read_excel(file,  skiprows=10, header=None, engine='openpyxl')

        # Добавление столбца с названием магазина
        df['Название'] = shop_name

        print('Удаляем колонки')
        self.drop_columns(df)

        print('Первый раз меняем названия колонок')
        self.change_colnames_v1(df)

        print('Меняем значения к Nan')
        self.to_nan(df)

        print('Добавляем и удаляем колонки')
        df_prepared = self.add_and_remove_columns(df)

        print('Удаляем колонки с заголовками чеков')
        self.drop_check_row(df_prepared)

        print('Финально меняем названия колонок')
        self.change_colnames_v2(df_prepared)

        print('Загрузка прошла успешно')
        return df_prepared

    def change_colnames_v2(self, df):
        # Переименовываем столбцы
        df = df.rename(columns={'Чек/Идентификатор': 'Идентификатор'})
        df = df[
            ['Чек', 'Дата', 'Время', 'Идентификатор', 'Название товара', 'Количество (шт/кг)', 'Сумма', 'Сумма скидки',
             'Полная сумма (шт/кг)', 'Сумма скидки на кг', 'Время на чек', 'Магазин']]

    def drop_check_row(self, df):
        # Удаляем строки с данными "Чек 1 от 14.11.2023 8:57:23"
        old_check_title_indexes = df[df['Чек/Идентификатор'].astype(str).str.contains('Чек')].index
        df.drop(labels=old_check_title_indexes, axis=0, inplace=True)

    def to_nan(self, df):
        # Заменяем Nan в столбцах на 0
        df['Сумма скидки'] = df['Сумма скидки'].fillna(0)
        df['Сумма скидки на кг'] = df['Сумма скидки на кг'].fillna(0)

    def drop_columns(self, df):
        df.drop(df.columns[[2, 3, 4, 5, 6, 8, 11, 12, 13, 14]], axis=1, inplace=True)

    def change_colnames_v1(self, df):
        colnames = ['Чек/Идентификатор', 'Название товара', 'Количество (шт/кг)', 'Сумма', 'Сумма скидки',
                    'Полная сумма (шт/кг)', 'Сумма скидки на кг', 'Время на чек', 'Магазин']
        df.columns = colnames

    def add_and_remove_columns(self, df):
        # Найти индексы строк, содержащих слово 'Чек' в столбце 'Чек/Идентификатор'
        indices_with_check = df[df['Чек/Идентификатор'].astype(str).str.contains('Чек')].index

        check_count = len(indices_with_check)
        print('Количество чеков = ', check_count)

        # Добавляем конечный индекс, чтобы последний чек тоже посчитался
        indexes = indices_with_check
        find_index = df[df['Чек/Идентификатор'].astype(str).str.contains('Итого')].index[0]
        indexes = indexes.append(pd.Index([find_index], dtype='int64'))

        # Добавляем искуственную колонку Чек и удаляем строки с названием и временем чека

        df_prepared = df.copy()

        # Создадим пустые списки новых строк с названием чека и
        new_check_column = []
        new_date_column = []
        new_time_column = []
        row_to_drop = []

        # Пройдем по индексам и удалил старую строку
        for i in range(len(indexes) - 1):
            # print(i)
            check_index = indexes[i]  # Индекс чека
            next_check_index = indexes[i + 1]  # Индекс следующего чека
            product_start_index = indexes[i] + 1  # Индекс начала продуктов

            check_title = df['Чек/Идентификатор'][check_index]
            date_and_time = df['Чек/Идентификатор'][check_index].split('от ')[1]
            # print(check_title)
            # print(check_index)
            # print(next_check_index)
            for j in range(check_index, next_check_index):
                new_check_column.append(check_title)
                full_date = datetime.strptime(date_and_time, '%d.%m.%Y %H:%M:%S')
                new_date_column.append(full_date.date())
                new_time_column.append(full_date.time())
                row_to_drop.append(check_index)

        # Удаляем крайнюю строку с итогами
        df_prepared = df_prepared.drop(df.index[-1])

        df_prepared['Чек'] = new_check_column
        df_prepared['Дата'] = new_date_column
        df_prepared['Дата'] = pd.to_datetime(df_prepared['Дата'])
        df_prepared['Время'] = new_time_column

        return df_prepared

    # Объединение всех датафреймов в один
    def combine_dataframes(self, dataframes):
        if len(dataframes) == 1:
            return dataframes[0]

        return pd.concat(dataframes, ignore_index=True)
