import logging
from datetime import date

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from data_quality_monitoring import create_data

store_dict = create_data()
app = FastAPI()


@app.get("/")
def get_nb_visitors(
    store_name: str = "Nancy",
    year: int = 2021,
    month: int = 1,
    day: int = 25,
    hour: int = 21,
    sensor_id: int | None = None,
) -> JSONResponse:
    # Check the year
    if year < 2020:
        return JSONResponse(status_code=404, content="No data before 2020")

    # Check the date
    try:
        requested_date = date(year, month, day)
    except ValueError as e:
        logging.error(f"Could not cast date: {e}")
        return JSONResponse(status_code=404, content="Enter a valid date")

    # Check the date is in the past
    if date.today() < requested_date:
        return JSONResponse(status_code=404, content="Choose a date in the past")
    # If no sensor choose return the visit for the whole store
    if hour > max(store_dict[store_name].sensors[0].open_hours):
        hour = 21
    if sensor_id is None:
        visit_counts = store_dict[store_name].get_store_traffic(requested_date, hour)
    elif sensor_id not in range(len(store_dict[store_name].sensors)):
        return JSONResponse(
            status_code=404,
            content=(
                f"Sensor #{sensor_id} does not exist. "
                f"This store only have {len(store_dict[store_name].sensors)} sensors."
            ),
        )
    else:
        visit_counts = store_dict[store_name].get_sensor_traffic(
            sensor_id, requested_date, hour
        )
    if visit_counts < 0 or hour < min(store_dict[store_name].sensors[0].open_hours):
        return JSONResponse(
            status_code=404, content="The store was closed try another date or hour."
        )
    return JSONResponse(status_code=200, content=visit_counts)
