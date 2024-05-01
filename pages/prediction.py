import streamlit as st
import pandas as pd
import os

from constants.constants import PREDICTION_PRODUCTS
from helpers.check_prepare_load_by_path import check_prepare_load_by_path
from prophet_helpers.load_models import load_models

from helpers.display_prediction import display_prediction
from prophet_helpers.build_base_dataframe import build_base_dataframe


@st.cache_data()
def file_load():
    return check_prepare_load_by_path()


# Получите текущий каталог (где находится файл prediction.py)
current_directory = os.path.dirname(os.path.realpath(__file__))
model_file_path = os.path.join(current_directory, '..', 'prophet_helpers', 'models')

st.set_page_config(page_title="Предсказывание", page_icon="🌍")

st.markdown("# Предсказывание")
st.sidebar.header("Параметры")

df = file_load()
models = load_models(model_file_path)

select_product = st.selectbox(
    "Выберите продукт",
    PREDICTION_PRODUCTS,
)

current_model = models[select_product]

predictions = st.sidebar.number_input(
    "Кол-во дней для предсказания",
    value=15,
    placeholder="Введите число"
)

future = current_model.make_future_dataframe(periods=predictions)
forecast = current_model.predict(future)

df_product = df.groupby(['Название товара', 'Магазин', 'Дата'])['Количество (шт/кг)'].sum().reset_index()
df_product = df_product.loc[df_product['Название товара'] == select_product]

data2 = build_base_dataframe(df_product)

display_prediction(data2, forecast, predictions)
