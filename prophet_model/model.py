from prophet import Prophet


def create_prophet_model(train, prediction):
    m = Prophet(
        daily_seasonality=False,
        weekly_seasonality=True
    )

    m.fit(train)

    future = m.make_future_dataframe(
        periods=prediction
    )

    forecast = m.predict(future)

    return forecast

