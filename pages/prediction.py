import pandas as pd
import streamlit as st
import os

from ar.display import display_prediction_ar
from ar.model import create_ar_model
from avg_moving.display import display_prediction_avg_moving
from avg_moving.model import create_avg_moving_model
from constants.constants import PREDICTION_PRODUCTS
from helpers.check_prepare_load_by_path import check_prepare_load_by_path
from helpers.get_top_correlations import get_top_correlations
from prophet_helpers.build_future_dataframe import build_future_dataframe
from prophet_helpers.load_models import load_prophet_models

from prophet_helpers.display_prediction import display_prediction_prophet
from prophet_helpers.build_base_dataframe import build_base_dataframe
from prophet_model.model import create_prophet_model
from sarimax_helpers.display_prediction import display_prediction_sarimax
from sarimax_helpers.load_models import load_sarimax_models
from sarimax_model.model import create_sarimax_model

ITEMS_COUNT = 50

# Получите текущий каталог (где находится файл prediction.py)
current_directory = os.path.dirname(os.path.realpath(__file__))

@st.cache_data()
def file_load():
    return pd.read_csv(
        os.path.join(current_directory, '..', 'data', 'day_sales_all_products.csv')
    )


prophet_model_file_path = os.path.join(current_directory, '..', 'prophet_helpers', 'models')
sarimax_model_file_path = os.path.join(current_directory, '..', 'sarimax_helpers', 'models')

st.set_page_config(page_title="Предсказывание", page_icon="🌍")

st.markdown("# Предсказывание")
st.sidebar.header("Параметры")

df = file_load()
prediction_models = {
    'Prophet':  load_prophet_models(prophet_model_file_path),
    'Sarimax': load_sarimax_models(sarimax_model_file_path),
}

item_counts = (df
               .groupby(['Название товара'])['Количество (шт/кг)'].sum()
               .sort_values(ascending=False).nlargest(ITEMS_COUNT))

popular_products = item_counts.index

select_product = st.selectbox(
    "Выберите продукт",
    popular_products,
)

try:
    current_models = {
        'Prophet': prediction_models['Prophet'][select_product],
        'Sarimax': prediction_models['Sarimax'][select_product],
    }
except KeyError as e:
    print('Ошибка, модель не найдена')
    current_models = None  # Присвоение значения None, если модель не найдена

predictions = st.sidebar.number_input(
    "Кол-во дней для предсказания",
    value=15,
    placeholder="Введите число"
)

future = build_future_dataframe(df, predictions)

df_product = df.groupby(['Название товара', 'Дата'])['Количество (шт/кг)'].sum().reset_index()
df_product = df_product.loc[df_product['Название товара'] == select_product]

base_df = build_base_dataframe(df_product)

# Correlation
n = 10
df_pivot = df.pivot_table(index='Дата', columns='Название товара', values='Количество (шт/кг)', aggfunc='sum', fill_value=0)

temp_product_correlation = get_top_correlations(df_pivot, select_product, n)
# st.write(temp_product_correlation.style.set_properties(**{'color': 'black'}))

# print(temp_product_correlation)
# st.title('Таблица товаров и коэффициентов')

st.write("Топ коррелирующих продуктов")
st.table(temp_product_correlation)

# avg_moving model
avg_moving_model_forecast = create_avg_moving_model(base_df, predictions)
print('IM here')
print(avg_moving_model_forecast)
total_count_prediction = int(avg_moving_model_forecast.values.sum())
display_prediction_avg_moving(base_df, avg_moving_model_forecast)
st.write('Итого за ' + str(predictions) + ' дней будет продано ' + str(total_count_prediction) + ' позиций')

# ar model
ar_model_forecast = create_ar_model(base_df, predictions)
display_prediction_ar(base_df, ar_model_forecast)
st.write('Итого за ' + str(predictions) + ' дней будет продано ' + str(round(ar_model_forecast.values[-predictions:].sum())) + ' позиций')


# prophet_model
prophet_model_forecast = create_prophet_model(base_df, predictions)
total_count_prediction = int(prophet_model_forecast['yhat'][-predictions:].sum())
display_prediction_prophet(base_df, prophet_model_forecast, predictions)
st.write('Итого за ' + str(predictions) + ' дней будет продано ' + str(total_count_prediction) + ' позиций')


# sarimax_model
sarimax_model_forecast = create_sarimax_model(base_df, predictions)
total_count_prediction = int(sarimax_model_forecast.values.sum())
display_prediction_sarimax(base_df, sarimax_model_forecast)
st.write('Итого за ' + str(predictions) + ' дней будет продано ' + str(total_count_prediction) + ' позиций')

    # if current_models['Prophet']:
    #     prophet_forecast = current_models['Prophet'].predict(future)
    #     total_count_prediction = int(prophet_forecast['yhat'][-predictions:].sum())
    #     display_prediction_prophet(base_df, prophet_forecast, predictions)
    #     st.write('Итого за ' + str(predictions) + ' дней будет продано ' + str(total_count_prediction))
    #
    # if current_models['Sarimax']:
    #     sarimax_forecast = current_models['Sarimax'].forecast(steps=predictions)
    #     sarimax_forecast.index = future['ds'][-predictions:]
    #
    #     display_prediction_sarimax(base_df, sarimax_forecast)
    #     st.write('Итого за ' + str(predictions) + ' дней будет продано ' + str(int(sarimax_forecast.values.sum())))
