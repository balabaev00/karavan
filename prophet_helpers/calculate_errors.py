from sklearn.metrics import mean_squared_error, mean_absolute_error
import numpy as np


def calculate_errors(df, predictions, forecast):
    # Подготовка данных для вычисления метрик
    y_true = df['y'][-predictions:]  # Фактические значения за последние 14 дней
    y_pred = forecast['yhat'][-predictions:]  # Прогнозные значения за последние 14 дней

    # Вычисление MSE и MAE
    mse = mean_squared_error(y_true, y_pred)
    mae = mean_absolute_error(y_true, y_pred)

    # Вычисление MAPE (Mean Absolute Percentage Error)
    mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100

    return mse, mae, mape
