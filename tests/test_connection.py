"""Prueba repetible del Hito 1: conexión a SQLite, esquema y flujo base.

Ejecutar desde la raíz del proyecto:
    python -m unittest discover -s tests -v
"""
import os
import sqlite3
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))


class SqliteBaseTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        os.environ["DB_ENGINE"] = "sqlite"
        os.environ["DB_NAME"] = os.path.join(self.tmp.name, "test.db")
        from persistence.create_db import create_tables
        create_tables()

    def tearDown(self):
        self.tmp.cleanup()

    def test_all_tables_are_created(self):
        connection = sqlite3.connect(os.environ["DB_NAME"])
        names = {r[0] for r in connection.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table'")}
        connection.close()
        expected = {"users", "destinations", "packages", "package_destinations",
                    "reservations", "reservation_progress"}
        self.assertTrue(expected.issubset(names))

    def test_foreign_keys_are_enforced(self):
        from persistence.base_dao import DatabaseError
        from persistence.reservation_dao import ReservationDAO
        with self.assertRaises(DatabaseError):
            ReservationDAO._write(
                "INSERT INTO reservations (user_id, package_id, reservation_date, "
                "travelers, total_paid, status) VALUES (?, ?, ?, ?, ?, ?)",
                (999, 999, "2026-01-01", 1, 100.0, "confirmed"), "insertar reserva")

    def test_password_is_stored_as_hash_and_login_works(self):
        from persistence.user_dao import UserDAO
        from services.auth import authenticate, register_client
        register_client("Ana Pérez", "Ana@Correo.cl", "clave-segura-1")
        stored = UserDAO.find_by_email("ana@correo.cl")
        self.assertNotEqual(stored.password_hash, "clave-segura-1")
        self.assertTrue(stored.password_hash.startswith("$2"))
        self.assertEqual(stored.role, "client")
        self.assertIsNotNone(authenticate("ana@correo.cl", "clave-segura-1"))
        self.assertIsNone(authenticate("ana@correo.cl", "otra-clave-1"))
        self.assertIsNone(authenticate("noexiste@correo.cl", "clave-segura-1"))

    def test_duplicate_email_is_rejected(self):
        from services.auth import register_client
        register_client("Ana Pérez", "ana@correo.cl", "clave-segura-1")
        with self.assertRaises(ValueError):
            register_client("Otra Ana", "ana@correo.cl", "clave-segura-2")

    def test_client_cannot_manage_destinations_but_admin_can(self):
        from persistence.destination_dao import DestinationDAO
        from services import destination_service as svc
        from services.auth import authenticate, create_admin, register_client
        register_client("Ana Pérez", "ana@correo.cl", "clave-segura-1")
        create_admin("Admin", "admin@va.cl", "admin-segura-1")
        client = authenticate("ana@correo.cl", "clave-segura-1")
        admin = authenticate("admin@va.cl", "admin-segura-1")

        with self.assertRaises(PermissionError):
            svc.create_destination(client, "Atacama", "Desierto", "Trekking", 100)

        created = svc.create_destination(admin, "Atacama", "Desierto", "Trekking", 100)
        self.assertEqual(len(svc.list_destinations(admin)), 1)

        # RF-03: un destino que está en un paquete no se puede eliminar
        DestinationDAO._write(
            "INSERT INTO packages (name, start_date, end_date, available_slots) "
            "VALUES (?, ?, ?, ?)", ("P1", "2026-12-01", "2026-12-10", 5), "crear paquete")
        DestinationDAO._write(
            "INSERT INTO package_destinations (package_id, destination_id, visit_order) "
            "VALUES (1, ?, 1)", (created.id,), "vincular destino")
        with self.assertRaises(ValueError):
            svc.delete_destination(admin, created.id)

    def test_negative_cost_is_rejected(self):
        from domain.destination import Destination
        with self.assertRaises(ValueError):
            Destination("X", "Y", "Z", -5)


if __name__ == "__main__":
    unittest.main()
