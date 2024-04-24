import pandas as pd


# Средняя сумма чека
def get_check_avg_sum(df: pd.DataFrame):
    return df.groupby(['Чек'])['Сумма'].sum().mean()


# Выручка
def get_revenue(df: pd.DataFrame):
    return df.groupby(['Чек'])['Сумма'].sum().sum()


# Количество чеков в датафрейме
def get_check_count(df: pd.DataFrame):
    df_checks = df.copy()
    # Удаляем строки с повторяющимся названием чека
    df_checks.drop_duplicates('Чек', inplace=True, keep='first')

    return df_checks.shape[0]


def get_most_popular_products(df: pd.DataFrame, count: int):
    return df['Название товара'].value_counts().sort_values(ascending=False).nlargest(count)
