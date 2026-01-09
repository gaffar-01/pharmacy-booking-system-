import sqlite3

def create_database():
    connection = sqlite3.connect("pharmacy.db")
    cursor = connection.cursor()

    # USERS TABLE
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('Patient', 'Staff')),
            password TEXT NOT NULL,
            answer TEXT NOT NULL
        )
    """)

    # SERVICES TABLE
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS services (
            service_id INTEGER PRIMARY KEY AUTOINCREMENT,
            service_name TEXT UNIQUE NOT NULL
        );
    """)

    # APPOINTMENTS TABLE
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            service_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            status TEXT NOT NULL CHECK(status IN ('Booked', 'Cancelled','Attended')),
            FOREIGN KEY(user_id) REFERENCES users(user_id),
            FOREIGN KEY(service_id) REFERENCES services(service_id)
        );
    """)

    connection.commit()
    connection.close()

create_database()

