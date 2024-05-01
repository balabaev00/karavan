import streamlit as st
import os

from constants.constants import PREDICTION_PRODUCTS
from helpers.check_prepare_load_by_path import check_prepare_load_by_path
from prophet_helpers.build_future_dataframe import build_future_dataframe
from prophet_helpers.load_models import load_prophet_models

from prophet_helpers.display_prediction import display_prediction_prophet
from prophet_helpers.build_base_dataframe import build_base_dataframe
from sarimax_helpers.display_prediction import display_prediction_sarimax
from sarimax_helpers.load_models import load_sarimax_models


@st.cache_data()
def file_load():
    return check_prepare_load_by_path()


# Получите текущий каталог (где находится файл prediction.py)
current_directory = os.path.dirname(os.path.realpath(__file__))
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

select_product = st.selectbox(
    "Выберите продукт",
    PREDICTION_PRODUCTS,
)

current_models = {
    'Prophet': prediction_models['Prophet'][select_product],
    'Sarimax': prediction_models['Sarimax'][select_product],
}

predictions = st.sidebar.number_input(
    "Кол-во дней для предсказания",
    value=15,
    placeholder="Введите число"
)

future = build_future_dataframe(df, predictions)

prophet_forecast = current_models['Prophet'].predict(future)
total_count_prediction = int(prophet_forecast['yhat'][-predictions:].sum())

df_product = df.groupby(['Название товара', 'Магазин', 'Дата'])['Количество (шт/кг)'].sum().reset_index()
df_product = df_product.loc[df_product['Название товара'] == select_product]

base_df = build_base_dataframe(df_product)

print(prophet_forecast)
display_prediction_prophet(base_df, prophet_forecast, predictions)

st.write('Итого за ' + str(predictions) + ' дней будет продано ' + str(total_count_prediction))

sarimax_forecast = current_models['Sarimax'].forecast(steps=predictions)
sarimax_forecast.index = future['ds'][-predictions:]

display_prediction_sarimax(base_df, sarimax_forecast)

st.write('Итого за ' + str(predictions) + ' дней будет продано ' + str(int(sarimax_forecast.values.sum())))
