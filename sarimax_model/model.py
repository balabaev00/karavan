import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX


def create_sarimax_model(train, prediction):
    # Обучение модели SARIMA
    order = (0, 1, 1)  # Параметры ARIMA
    seasonal_order = (1, 1, 1, 12)  # Сезонные параметры ARIMA

    model = SARIMAX(train['y'], order=order, seasonal_order=seasonal_order)
    fitted_model = model.fit()

    # Прогнозирование
    forecast = fitted_model.predict(start=len(train), end=len(train) + prediction)

    start_date = pd.Timestamp(train['ds'].max()) + pd.Timedelta(days=1)
    end_date = start_date + pd.Timedelta(days=prediction)

    forecast.index = pd.date_range(start=start_date, end=end_date)

    return forecast
