"""Pruebas de las clases de dominio (coherentes con el diagrama de clases UML)."""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from domain.destination import Destination
from domain.package import Package
from domain.progress import ReservationProgress
from domain.reservation import Reservation


class DomainTest(unittest.TestCase):
    def test_package_cost_is_sum_of_destinations(self):  # RF-06
        package = Package("Norte", "2026-12-01", "2026-12-10", 5)
        package.destinations = [Destination("A", "d", "a", 100), Destination("B", "d", "a", 150)]
        self.assertEqual(package.calculate_total_cost(), 250)

    def test_package_rejects_end_before_start(self):  # RF-05
        with self.assertRaises(ValueError):
            Package("Norte", "2026-12-10", "2026-12-01", 5)

    def test_package_availability(self):  # RF-08
        self.assertTrue(Package("N", "2026-12-01", "2026-12-02", 1).is_available())
        self.assertFalse(Package("N", "2026-12-01", "2026-12-02", 0).is_available())

    def test_reservation_total_and_validation(self):  # RF-11
        reservation = Reservation(1, 1, "2026-11-25", 3, 0)
        self.assertEqual(reservation.calculate_total(250), 750)
        with self.assertRaises(ValueError):
            Reservation(1, 1, "2026-11-25", 0, 0)

    def test_progress_complete_requires_date(self):  # RF-13
        progress = ReservationProgress(1, 1)
        progress.start()
        self.assertEqual(progress.status, "in_progress")
        with self.assertRaises(ValueError):
            progress.complete("")
        progress.complete("2026-12-03")
        self.assertEqual((progress.status, progress.registered_date), ("completed", "2026-12-03"))


if __name__ == "__main__":
    unittest.main()
