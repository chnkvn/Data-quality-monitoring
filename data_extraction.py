import sys
from datetime import date

import requests

year, month, day = [int(v) for v in sys.argv[1].split("-")]
date_ = date(year, month, day)
assert type(date_) == date
print(date_.year, type(date_.year))
def request_api(day:date = date_, hour=21, url="http://127.0.0.1:8000/"):
    """Request information from an API"""
    params = {'year':day.year,
              "month":day.month,
              "day":day.day,
              "hour":hour}
    r = requests.get(url, params=params)
    return r.content
print(request_api(date_, 7))
