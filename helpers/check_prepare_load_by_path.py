import pandas as pd
import os

from enums.shop_name_enum import ShopName

FILE_PATH = './data/'


def check_prepare_load_by_path(folder_path=FILE_PATH, shop_name=ShopName.Babushkina.value):
    # Список для хранения данных из всех файлов
    dataframes = []
    # Флаг для отслеживания, был ли уже загружен первый датафрейм
    first_loaded = False

    # Чтение файлов из папки
    for filename in os.listdir(folder_path):
        if filename.endswith('.xlsx'):
            fileshop_name = filename.split('_')[0].title()
            if fileshop_name == shop_name:
                print(f"Загружается файл {filename}")

                # Загрузка данных из файла
                filepath = os.path.join(folder_path, filename)
                temp_df = pd.read_excel(filepath)

                # Если это первый загруженный датафрейм, сохраняем его заголовки
                if not first_loaded:
                    first_loaded = True
                    dataframes.append(temp_df)
                else:
                    # Добавляем датафрейм без заголовков
                    dataframes.append(pd.DataFrame(temp_df.values, columns=dataframes[0].columns))
    # Склейка датафреймов
    df = pd.concat(dataframes, ignore_index=True)

    df['Чек/Идентификатор'] = pd.to_numeric(df['Чек/Идентификатор'], errors='coerce')
    df['Сумма'] = pd.to_numeric(df['Сумма'], errors='coerce')
    df['Сумма скидки'] = pd.to_numeric(df['Сумма скидки'], errors='coerce')
    df['Полная сумма (шт/кг)'] = pd.to_numeric(df['Полная сумма (шт/кг)'], errors='coerce')
    df['Сумма скидки на кг'] = pd.to_numeric(df['Сумма скидки на кг'], errors='coerce')
    df['Время на чек'] = pd.to_numeric(df['Время на чек'], errors='coerce')
    df['Количество (шт/кг)'] = pd.to_numeric(df['Количество (шт/кг)'], errors='coerce')

    # Если есть хотя бы один загруженный датафрейм, возвращаем результат
    if len(df) > 0:
        return df
    else:
        return None  # Возвращаем None, если нет данных
