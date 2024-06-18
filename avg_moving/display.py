import plotly.graph_objs as go
from plotly.subplots import make_subplots
import streamlit as st

def display_prediction_avg_moving(df, forecast):
    # Создаем графики
    fact_trace = go.Scatter(x=df['ds'], y=df['y'], name='Факт', mode='lines+markers')
    pred_trace = go.Scatter(x=forecast.index, y=forecast['y'], name='Прогноз', line=dict(color='red'))


    # Создаем подзаголовок для прогноза и факта
    fig = make_subplots(rows=1, cols=1)
    fig.add_trace(fact_trace)
    fig.add_trace(pred_trace)

    # Обновляем макет и отображаем график
    fig.update_layout(title='Прогноз простое скользящее среднее', xaxis_title='Дата', yaxis_title='Значение', height=500, width=700)
    st.plotly_chart(fig)
