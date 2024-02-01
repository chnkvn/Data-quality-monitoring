import sys
from datetime import date, timedelta
import numpy as np
from attrs import define, field


@define
class Sensor:
    """Create a sensor that returns the number
    of visitors given a date and an hour."""

    avg_visit: int = field(converter=int)
    std_visit: float = field(converter=float)
    perc_break: float = field(converter=float, default=0.015)
    perc_malfunction: float = field(converter=float, default=0.035)
    open_hours = list(range(9, 22))

    def simulate_visit_count(self, business_date: date) -> int:
        """Simulate the number of person detected by the sensor given a date and an hour"""

        # For reprocubility
        np.random.seed(seed=business_date.toordinal())

        # Get weekday of the business day
        weekday = business_date.weekday()

        # Generate the visitor counts over the working hours
        visits = np.random.normal(
            self.avg_visit, self.std_visit, size=len(self.open_hours)
        ) / len(self.open_hours)

        # More traffic on wednesdays (2), fridays (4), saturdays (5)
        if weekday == 2:
            visits *= 1.15
        elif weekday == 4:
            visits *= 1.2
        elif weekday == 5:
            visits *= 1.35
        # visitor count is set to -1 on sundays
        elif weekday == 6:
            visits *= 0
            visits -= 1
        return visits

    def get_visit_count(self, business_date: date, hour: int) -> int:
        """Returns the number of visitors from the store opening hour to the hour passed in parameters."""
        # For reprocubility
        np.random.seed(seed=business_date.toordinal())

        visitors_count = 0
        proba_malfunction = np.random.random()

        # The sensor can break sometimes
        # Also return 0 when hour in closing hours
        if proba_malfunction < self.perc_break or hour not in self.open_hours:
            return visitors_count
        if business_date.weekday() == 6:
            return -1
        visits = self.simulate_visit_count(business_date)
        # The sensor can also malfunction
        if proba_malfunction < self.perc_malfunction:
            visits *= 0.2  # make it so bad we can detect it ;)
        visits = np.floor(visits)
        for hour_, visit_count in zip(self.open_hours, visits):
            if hour_ == hour:
                visitors_count = visit_count
                break
        return int(visitors_count)


if __name__ == "__main__":
    if len(sys.argv) > 2:
        year, month, day = [int(v) for v in sys.argv[1].split("-")]
        hour = int(sys.argv[2])
    else:
        year, month, day = 2023, 10, 25
        hour = 18
    queried_date = date(year, month, day)

    captor = Sensor(1500, 150)
    print(captor.get_visit_count(queried_date, hour))
