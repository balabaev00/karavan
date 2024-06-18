import pandas as pd


def create_avg_moving_model(train, prediction, window_size=7):
    predictions = []
    data_copy = train.copy()

    for i in range(prediction):
        # Рассчитываем скользящее среднее для последних window_size дней
        forecast = data_copy['y'].rolling(window=window_size).mean().iloc[-1]
        print('Предсказывания', forecast)
        predictions.append(forecast)

        # Добавляем новое значение в data_copy для дальнейшего предсказания
        new_date = data_copy['ds'].max() + pd.Timedelta(days=1)
        new_row = pd.DataFrame({'ds': [new_date], 'y': [forecast]})
        data_copy = pd.concat([data_copy, new_row], ignore_index=True)

    forecast_df = pd.DataFrame({'ds': data_copy['ds'].iloc[-prediction:], 'y': predictions})
    forecast_df.set_index('ds', inplace=True)

    return forecast_df

