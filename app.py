import streamlit as st
import pandas as pd
import plotly.express as px

from constants.constants import CHECK_FOLDER
from enums.shop_name_enum import ShopName
from helpers.check_loader import CheckLoader
from helpers.check_helper import *
from helpers.check_prepare_load import check_prepare_load


class CaravanApp:
    def __init__(self):
        self.loader = CheckLoader(CHECK_FOLDER)
        self.data = pd.DataFrame()
        self.configure_page()
        self.load_custom_style()
        self.loaded_files = []

    def configure_page(self):
        st.set_page_config(page_title='Статистика магазинов', layout='wide', initial_sidebar_state='expanded',
                           page_icon=None)

    def load_custom_style(self):
        with open('style.css') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    def setup_shop_names(self):
        self.shop_names = st.sidebar.multiselect(
            'Магазин',
            sorted([shop.value for shop in ShopName]),
            placeholder='Выберите нужные магазины'
        )

    def get_current_data(self):
        return self.data

    @st.cache(allow_output_mutation=True)
    def file_load(self, uploaded_files):
        dataframes = []

        for file in uploaded_files:
            file_shop_name = file.name.split('_')[0].title()
            dataframes.append(self.loader.file_to_df(file, file_shop_name))
            self.loaded_files.append(file.name)

        return self.loader.combine_dataframes(dataframes)

    def update_metrics_and_graphics(self):
        self.display_metrics()
        self.display_charts()

    # Отрисовка метрик
    def display_metrics(self):
        df = self.get_current_data()
        st.markdown('### Метрики')
        col1, col2, col3 = st.columns(3)
        col1.metric("Выручка", f'{get_revenue(df):,.2f}')
        col2.metric("Средний чек", f'{get_check_avg_sum(df):,.2f}')
        col3.metric("Количество чеков", get_check_count(df))

    # Отрисовка графиков
    def display_charts(self):
        # Загрузка нескольких файлов
        uploaded_files = st.file_uploader("Выберите файлы", type=['xlsx', 'csv'], accept_multiple_files=True)

        # Проверка, были ли файлы загружены
        if uploaded_files is not None and len(uploaded_files) > 0:
            self.data = check_prepare_load(uploaded_files)

        # c1, c2 = st.columns((7, 3))
        # with c1:
        #     st.markdown('### Тепловая карта')
        #     plost.time_hist(data=seattle_weather, date='date', x_unit='week', y_unit='day', color=self.time_hist_color,
        #                     aggregate='median', legend=None, height=345, use_container_width=True)
        # with c2:
        #     st.markdown('### Круговая диаграмма')
        #     plost.donut_chart(data=stocks, theta=self.donut_theta, color='company', legend='bottom',
        #                       use_container_width=True)
        data = self.get_current_data()
        if isinstance(data, pd.DataFrame) and not data.empty:
            self.display_metrics()
            self.display_sum_check_chart()
            self.display_avg_sum_check_chart()
            self.display_the_most_popular_products_chart()

    # График средней суммы чека
    def display_avg_sum_check_chart(self):
        avg_check_sum_days = self.data.groupby(['Чек', 'Дата', 'Магазин'])['Сумма'].sum().groupby(['Дата', 'Магазин']).mean().unstack()
        st.markdown('### Средняя сумма чека по дням')
        st.line_chart(avg_check_sum_days)

    # График выручки
    def display_sum_check_chart(self):
        df = self.get_current_data()
        st.markdown('### График выручки')
        check_sum = df.groupby(['Чек', 'Дата', 'Магазин'])['Сумма'].sum().groupby(['Дата','Магазин']).sum().unstack()
        st.line_chart(check_sum)


    # График самых популярных товаров
    def display_the_most_popular_products_chart(self):
        df = self.get_current_data()
        top_products = get_most_popular_products(df, 10)
        st.markdown('### Количество покупок самых популярных товаров')
        fig = px.bar(
            top_products,
            y=top_products.index,
            x=top_products.values,
            orientation='h',
            template="plotly_white",
            labels={'x': 'Количество покупок', 'index': 'Название товара'}
        )

        fig.update_layout(yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig)

    def run(self):
        self.display_charts()


if __name__ == "__main__":
    app = CaravanApp()
    app.run()
