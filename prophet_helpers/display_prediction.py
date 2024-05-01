import streamlit as st
import plotly.graph_objs as go
from plotly.subplots import make_subplots


def display_prediction_prophet(df, forecast, test_n):
    # Создание графиков
    fact_trace = go.Scatter(x=df['ds'], y=df['y'], name='Факт', mode='lines+markers')
    pred_trace = go.Scatter(x=forecast['ds'][-test_n:], y=forecast['yhat'][-test_n:], name='Прогноз', line=dict(color='red'))
    upper_trace = go.Scatter(x=forecast['ds'], y=forecast['yhat_upper'], fill='tonexty', mode='none',
                             name='Верхняя граница')
    lower_trace = go.Scatter(x=forecast['ds'], y=forecast['yhat_lower'], fill='tonexty', mode='none',
                             name='Нижняя граница')
    trend_trace = go.Scatter(x=forecast['ds'], y=forecast['trend'], name='Тренд')

    # Создание подзаголовка для прогноза и факта
    fig = make_subplots(rows=1, cols=1)
    fig.add_trace(fact_trace)
    fig.add_trace(pred_trace)
    fig.add_trace(upper_trace)
    fig.add_trace(lower_trace)
    fig.add_trace(trend_trace)

    # Обновление макета и отображение графика
    fig.update_layout(title='Прогноз Prophet', xaxis_title='Дата', yaxis_title='Значение', height=500,
                      width=700)  # Уменьшаем размер графика
    st.plotly_chart(fig)
