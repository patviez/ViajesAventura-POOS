import os
import sqlite3
from dotenv import load_dotenv
load_dotenv()

DB_ERRORS = [sqlite3.Error, ValueError, OverflowError]
try:
    import pymysql
    DB_ERRORS.append(pymysql.MySQLError)
except ImportError:
    pymysql = None
DB_ERRORS = tuple(DB_ERRORS)


def get_engine():
    return os.getenv("DB_ENGINE", "sqlite").lower()


def open_connection():
    engine = get_engine()

    if engine == "sqlite":
        connection = sqlite3.connect(os.getenv("DB_NAME", "viajes_aventura.db"))
        connection.execute("PRAGMA foreign_keys = ON")  # SQLite lo trae apagado
        return connection

    if engine == "mysql":
        if pymysql is None:
            raise RuntimeError("Instale PyMySQL para usar MySQL.")
        return pymysql.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=int(os.getenv("DB_PORT", "3306")),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            charset="utf8mb4",
        )

    raise ValueError(f"Motor no soportado: {engine}")


def placeholder():
    return "?" if get_engine() == "sqlite" else "%s"
