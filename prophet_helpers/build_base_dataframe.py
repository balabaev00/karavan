import pandas as pd


def build_base_dataframe(df_product):
    data2 = pd.DataFrame()
    data2['y'] = df_product['Количество (шт/кг)']
    data2['ds'] = pd.to_datetime(df_product['Дата'])

    # data2.set_index('ds', inplace=True)

    return data2
