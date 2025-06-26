
import pandas as pd
from datetime import datetime
from homework.batch import prepare_data

def dt(hour, minute, second=0):
    return datetime(2023, 1, 1, hour, minute, second)

def test_prepare_data():
    data = [
        (None, None, dt(1, 1), dt(1, 10)),
        (1, 1, dt(1, 2), dt(1, 10)),
        (1, None, dt(1, 2, 0), dt(1, 2, 59)),
        (3, 4, dt(1, 2, 0), dt(2, 2, 1)),      
    ]
    columns = ['PULocationID', 'DOLocationID', 'tpep_pickup_datetime', 'tpep_dropoff_datetime']
    df = pd.DataFrame(data, columns=columns)
    
    categorical = ['PULocationID', 'DOLocationID']
    df_actual = prepare_data(df, categorical)
    
    data_expected = [
        ('-1', '-1', dt(1, 1), dt(1, 10)),
        ('1', '1', dt(1, 2), dt(1, 10)),
    ]
    columns_expected = ['PULocationID', 'DOLocationID', 'tpep_pickup_datetime', 'tpep_dropoff_datetime']
    df_expected = pd.DataFrame(data_expected, columns=columns_expected)

    # We need to convert the datatypes of the expected dataframe to match the actual one
    df_expected[['PULocationID', 'DOLocationID']] = df_expected[['PULocationID', 'DOLocationID']].astype(str)
    df_expected['tpep_pickup_datetime'] = pd.to_datetime(df_expected['tpep_pickup_datetime'])
    df_expected['tpep_dropoff_datetime'] = pd.to_datetime(df_expected['tpep_dropoff_datetime'])
    
    # Add the duration column to the expected dataframe
    df_expected['duration'] = (df_expected['tpep_dropoff_datetime'] - df_expected['tpep_pickup_datetime']).dt.total_seconds() / 60

    assert df_actual.shape[0] == 2
    assert df_actual.to_dict(orient='records') == df_expected.to_dict(orient='records')

