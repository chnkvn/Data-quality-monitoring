from datetime import date

import numpy as np
from attrs import define, field
from data_quality_monitoring.src.sensor import Sensor


@define
class Store:
    name: str = field(converter=str)
    avg_visit: int = field(converter=int)
    std_visit: float = field(converter=float)
    perc_malfunction: float = field(default=0)
    perc_break: float = field(default=0)
    sensors = field(init=False)

    def __attrs_post_init__(self):
        # To always get the same result when asking for the same store
        seed = np.sum(list(self.name.encode("ascii")))
        np.random.seed(seed=seed)
        # Let assume every store has 5 captors
        traffic_percentage = {0.49, 0.31, 0.1, 0.07, 0.03}
        self.sensors = [
            Sensor(
                percent * self.avg_visit,
                percent * self.std_visit,
                self.perc_break,
                self.perc_malfunction,
            )
            for percent in traffic_percentage
        ]

    def get_sensor_traffic(
        self, sensor_id: int, requested_date: date, hour: int
    ) -> int:
        """Return the traffic of a sensor given a date and an hour"""
        return self.sensors[sensor_id].get_visit_count(requested_date, hour)

    def get_store_traffic(self, requested_date: date, hour: int) -> int:
        """Return the traffic of all the sensors given a date and an hour"""
        traffic = sum(
            sensor.get_visit_count(requested_date, hour) for sensor in self.sensors
        )
        return traffic


if __name__ == "__main__":
    lille_store = Store("Test", 1200, 300)
    visits = lille_store.get_store_traffic(date(2023, 12, 21), 18)
    print(visits)
