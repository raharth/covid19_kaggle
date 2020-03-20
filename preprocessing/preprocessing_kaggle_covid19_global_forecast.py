import pandas as pd


def aggregate_on_country_level():
    data_frame = pd.read_csv('./data/raw_data/kaggle_covid19_global_forecasting_week_1/train.csv')

    new_data_frame = data_frame.groupby(
        ['Country/Region', 'Date']
    ).agg(
        Lat=('Lat', 'mean'),
        Long=('Long', 'mean'),
        ConfirmedCases=('ConfirmedCases', sum),
        Fatalities= ('Fatalities', sum)
    )

    new_data_frame.to_csv('./data/preprocessed_data/covid19_global_forecast/country_train.csv')


if __name__ == '__main__':
    aggregate_on_country_level()