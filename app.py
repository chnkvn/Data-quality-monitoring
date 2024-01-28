import logging
from datetime import date

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from src.sensor import Sensor

sensor = Sensor(5000, 750)
app = FastAPI()


@app.get("/")
def get_nb_visitors(year: int, month: int, day: int, hour: int = 21) -> JSONResponse:
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
    if hour > max(sensor.open_hours):
        visit_counts = sensor.get_visit_count(requested_date, 21)
    else:
        visit_counts = sensor.get_visit_count(requested_date, hour)
    if visit_counts < 0 or hour < min(sensor.open_hours):
        return JSONResponse(
            status_code=404, content="The store was closed try another date or hour."
        )
    return JSONResponse(status_code=200, content=visit_counts)
