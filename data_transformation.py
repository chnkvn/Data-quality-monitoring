from pathlib import Path

import pandas as pd
import duckdb

def read_data() -> pd.DataFrame:
    df = pd.DataFrame()
    raw_data_folder = Path.cwd().joinpath('data', 'raw')
    # Concatenate all csv into one dataframe
    for file in raw_data_folder.glob('*.csv'):
        csv_path = raw_data_folder.joinpath(file)
        df = pd.concat([df, pd.read_csv(csv_path)])

    # Remove duplicate rows
    df = df.drop_duplicates()
    # count column is composed of str values
    # Keep only the numbers, replace others values by NaN
    df['count'] = df['count'].str.replace(r"b'(\d+| )'",r'\1', regex=True)
    df['count'] = pd.to_numeric(df['count'], errors="coerce")
    print(df.head())
    print(df.shape)
    return df

def get_daily_traffic_per_store(df:pd.DataFrame) -> pd.DataFrame:
    """Keep rows where:
    - units value is equal to visitor
    - sensor_id is not a null value"""
    query = """SELECT date, store, sum(count) as traffic
    FROM df
    WHERE units == 'visitors' AND sensor_id is not NULL
    GROUP BY date, store
    ORDER BY date, store""" 
    return duckdb.sql(query).df()

if __name__ == '__main__':
   df =  read_data()
   df1 = get_daily_traffic_per_store(df)
   print(df1.head(10))
