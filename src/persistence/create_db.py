from persistence.connection import get_engine, open_connection

SQLITE_STATEMENTS = [
    """CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        role TEXT NOT NULL CHECK (role IN ('admin', 'client'))
    )""",
    """CREATE TABLE IF NOT EXISTS destinations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT NOT NULL,
        activities TEXT NOT NULL,
        base_cost REAL NOT NULL CHECK (base_cost >= 0)
    )""",
    """CREATE TABLE IF NOT EXISTS packages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        start_date TEXT NOT NULL,
        end_date TEXT NOT NULL,
        available_slots INTEGER NOT NULL CHECK (available_slots >= 0),
        CHECK (end_date >= start_date)
    )""",
    """CREATE TABLE IF NOT EXISTS package_destinations (
        package_id INTEGER NOT NULL,
        destination_id INTEGER NOT NULL,
        visit_order INTEGER NOT NULL,
        PRIMARY KEY (package_id, destination_id),
        FOREIGN KEY (package_id) REFERENCES packages(id),
        FOREIGN KEY (destination_id) REFERENCES destinations(id)
    )""",
    """CREATE TABLE IF NOT EXISTS reservations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        package_id INTEGER NOT NULL,
        reservation_date TEXT NOT NULL,
        travelers INTEGER NOT NULL CHECK (travelers > 0),
        total_paid REAL NOT NULL,
        status TEXT NOT NULL CHECK (status IN ('confirmed', 'cancelled')),
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (package_id) REFERENCES packages(id)
    )""",
    """CREATE TABLE IF NOT EXISTS reservation_progress (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        reservation_id INTEGER NOT NULL,
        destination_id INTEGER NOT NULL,
        status TEXT NOT NULL CHECK (status IN ('pending', 'in_progress', 'completed')),
        registered_date TEXT,
        UNIQUE (reservation_id, destination_id),
        FOREIGN KEY (reservation_id) REFERENCES reservations(id),
        FOREIGN KEY (destination_id) REFERENCES destinations(id)
    )""",
]


def create_tables():
    engine = get_engine()
    if engine != "sqlite":
        raise NotImplementedError("El esquema MySQL se agrega en el Hito 2.")

    connection = open_connection()
    try:
        cursor = connection.cursor()
        for statement in SQLITE_STATEMENTS:
            cursor.execute(statement)
        connection.commit()
    finally:
        connection.close()
