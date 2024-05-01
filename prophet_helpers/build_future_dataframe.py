import pandas as pd



def build_future_dataframe(df, prediction):
    earliest_date = pd.Timestamp(df['Дата'].min())
    latest_date = pd.Timestamp(df['Дата'].max())

    march_dates = pd.date_range(start=earliest_date, end=latest_date + pd.Timedelta(days=prediction))
    future = pd.DataFrame({'ds': march_dates})

    return future
