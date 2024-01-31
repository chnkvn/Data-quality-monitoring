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
    return df

def get_daily_traffic_per_store(df:pd.DataFrame) -> pd.DataFrame:
    """Keep rows where:
    - units value is equal to visitor
    - sensor_id is not a null value"""
    query = """SELECT date, store, sensor_id, weekday, sum(count) as daily_traffic FROM df
    WHERE units == 'visitors' and sensor_id IS NOT NULL
    GROUP BY date, weekday, store, sensor_id
    ORDER BY date, store, sensor_id
    """
    result_df = duckdb.sql(query).df()
    return result_df

def traffic_average_week(df:pd.DataFrame, n_week:int = 4):
    """Compute the moving average over the last $n_weeks weeks"""
    query = f"""
    SELECT date,
    store,
    weekday,
    sensor_id,
daily_traffic,
    AVG(daily_traffic)
    OVER(PARTITION BY weekday, store, sensor_id
    ORDER BY date
    ROWS BETWEEN  {n_week-1} PRECEDING AND CURRENT ROW)
    AS avg_n_weeks
    from df
    ORDER BY date, sensor_id, store
    """
    return duckdb.sql(query).df()

def pct_traffic_average_week(df:pd.DataFrame, n_week:int = 4):
    """Compute the percentage change between the moving average
    and the average of the current week"""
    query = f"""
    SELECT date, store, weekday, sensor_id,
    daily_traffic, avg_n_weeks,
    LAG(avg_n_weeks)
    OVER(PARTITION BY weekday, store, sensor_id
    ORDER BY date)  AS lag_avg_n_weeks,
    (100*(avg_n_weeks - lag_avg_n_weeks)/lag_avg_n_weeks) as pct_change
    from df
    """
    return duckdb.sql(query).df()

def save_df_to_parquet(df:pd.DataFrame):
    """Create the folder filtered in data/ and save the dataframe to a parquet file"""
    save_path = 'data/filtered'
    Path(save_path).mkdir(parents=True, exist_ok=True)
    df.to_parquet(Path(save_path, 'df.parquet.gzip'),
              compression='gzip', index=False)

def generate_filtered_data():
    df =  read_data()
    df= get_daily_traffic_per_store(df)
    df = traffic_average_week(df)
    df = pct_traffic_average_week(df)
    save_df_to_parquet(df)

if __name__ == '__main__':
   generate_filtered_data()
