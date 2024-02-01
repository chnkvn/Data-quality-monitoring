import sys
from pathlib import Path
from datetime import date, timedelta
import pandas as pd
import requests

date_ex = date(2023, 1, 25)


def request_api(
    store_name: str = "Nancy",
    day: date = date_ex,
    hour: int = 21,
    sensor_id: int = 0,
    url="http://127.0.0.1:8000/",
):
    """Request information from an API"""
    if len(sys.argv) > 1:
        store_name: str = sys.argv[1]
        day: date = date(*tuple(int(v) for v in sys.argv[2].split("-")))
        hour: int = sys.argv[3]
        sensor_id: int = sys.argv[4]
    assert type(day) == date
    params = {
        "store_name": store_name,
        "year": day.year,
        "month": day.month,
        "day": day.day,
        "hour": hour,
        "sensor_id": sensor_id,
    }
    r = requests.get(url, params=params)
    return r.content


def generate_csv():
    """Generate csv containing sensors data, 1 csv per month"""

    # Create data/raw if it does not exist
    save_path = "data/raw"
    Path(save_path).mkdir(parents=True, exist_ok=True)

    # Generate dataframe  containing the data for each month, until we reach the current date
    current_day = date(2020, 1, 1)
    data = []
    while current_day < date.today():
        for store in {"Nancy", "Paris", "Lille", "Cholet", "Cabourg"}:
            for hour in range(9, 22):
                for sensor_id in range(5):
                    data.append(
                        [
                            current_day,
                            hour,
                            store,
                            sensor_id,
                            request_api(store, current_day, hour, sensor_id),
                            "visitors",
                            current_day.weekday(),
                        ]
                    )
        next_day = current_day + timedelta(days=1)
        # if new month, generate and save the dataframe
        if next_day.month > current_day.month:
            df = pd.DataFrame(data)
            df.rename(
                columns={
                    0: "date",
                    1: "hour",
                    2: "store",
                    3: "sensor_id",
                    4: "count",
                    5: "units",
                    6: "weekday",
                },
                inplace=True,
            )
            noise_df1 = df.sample(frac=0.1)
            noise_df1["units"] = "items"
            noise_df2 = df.sample(frac=0.15)
            noise_df2["sensor_id"] = "NULL"
            dataframe = pd.concat([df, noise_df1, noise_df2]).sample(frac=1)
            dataframe.to_csv(
                f"{save_path}/{current_day.year}-{current_day.month:02d}.csv",
                index=False,
            )
            # reset the list containing the data
            data = []
        # extract data about the next day
        current_day = next_day
    return


if __name__ == "__main__":
    generate_csv()
