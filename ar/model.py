import pandas as pd
from statsmodels.tsa.ar_model import AutoReg


def create_ar_model(train, prediction, lag=30):
    model = AutoReg(train['y'], lags=lag)
    model_fit = model.fit()

    forecast = model_fit.predict(start=len(train['ds']), end=len(train['ds']) + prediction, dynamic=False)

    start_date = pd.Timestamp(train['ds'].max()) + pd.Timedelta(days=1)
    end_date = start_date + pd.Timedelta(days=prediction)

    forecast.index = pd.date_range(start=start_date, end=end_date)
    return forecast
