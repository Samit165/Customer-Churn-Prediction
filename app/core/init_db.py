"""
==========================================================
ChurnGuard
Database Initialization
==========================================================
Creates the SQLite database and default admin account.
"""

import sqlite3
import bcrypt
from pathlib import Path

# ---------------------------------------------------------
# Database Path
# ---------------------------------------------------------

DB_PATH = (
    Path(__file__).parent.parent
    / "database"
    / "users.db"
)

DB_PATH.parent.mkdir(parents=True, exist_ok=True)


def create_database():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            username TEXT UNIQUE NOT NULL,

            password_hash TEXT NOT NULL,

            full_name TEXT NOT NULL,

            email TEXT UNIQUE,

            role TEXT NOT NULL,

            last_login TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
        """
    )

    cursor.execute(
        "SELECT * FROM users WHERE username=?",
        ("admin",),
    )

    user = cursor.fetchone()

    if user is None:

        hashed_password = bcrypt.hashpw(
            "admin123".encode(),
            bcrypt.gensalt(),
        ).decode()

        cursor.execute(
            """
            INSERT INTO users
            (
                username,
                password_hash,
                full_name,
                email,
                role
            )
            VALUES
            (?, ?, ?, ?, ?)
            """,
            (
                "admin",
                hashed_password,
                "System Administrator",
                "admin@churnguard.com",
                "Admin",
            ),
        )

        print("✓ Default admin user created.")

    conn.commit()
    conn.close()

    print("✓ Database initialized successfully.")


if __name__ == "__main__":
    create_database()