import unittest
from datetime import date

from data_quality_monitoring.src.store import Store


class TestStore(unittest.TestCase):
    def test_get_store_traffic(self):
        lille_store = Store("Test", 1200, 300)
        visits = lille_store.get_store_traffic(date(2023, 12, 21), 18)

        self.assertEqual(visits, 111)

    def test_get_sensor_traffic(self):
        lille_store = Store("Test", 1200, 300)
        visits = lille_store.get_sensor_traffic(3, date(2023, 12, 21), 18)

        self.assertEqual(visits, 35)

    def test_sunday_closed(self):
        lille_store = Store("Test", 1200, 300)
        visits = lille_store.get_sensor_traffic(2, date(2024, 1, 7), 18)
        self.assertEqual(visits, -1)


if __name__ == "__main__":
    unittest.main()
