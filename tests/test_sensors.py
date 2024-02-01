import unittest
from datetime import date

import numpy as np
from data_quality_monitoring.src.sensor import Sensor


class TestVisitSensor(unittest.TestCase):
    def test_weekdays_open(self):
        for test_day in range(11, 17):
            with self.subTest(i=test_day):
                visit_sensor = Sensor(1200, 300)
                visit_count = visit_sensor.simulate_visit_count(date(2023, 9, test_day))
                self.assertFalse(-1 in set(visit_count))

    def test_sunday_closed(self):
        visit_sensor = Sensor(1200, 300)
        visit_count = visit_sensor.simulate_visit_count(date(2023, 9, 17))
        self.assertEqual(set(visit_count), {-1})

    def test_with_break(self):
        visit_sensor = Sensor(1500, 150, perc_break=15)
        visit_count = visit_sensor.get_visit_count(date(2023, 10, 12), 20)
        self.assertEqual(visit_count, 0)

    def test_with_malfunction(self):
        visit_sensor = Sensor(1500, 150, perc_malfunction=15)
        visit_count = visit_sensor.get_visit_count(date(2023, 10, 12), 20)
        self.assertEqual(visit_count, 20)


if __name__ == "__main__":
    unittest.main()
