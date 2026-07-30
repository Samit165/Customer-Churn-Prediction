"""
database.py
-----------------------------
Database management for ChurnGuard.

Responsibilities:
- Initialize SQLite database
- Password hashing using bcrypt
- User authentication
- User management
- Activity logging
- Prediction logging
"""

import sqlite3
from pathlib import Path
from datetime import datetime

import bcrypt

# --------------------------------------------------
# Database Configuration
# --------------------------------------------------

from core.config import DATABASE_DIR, DATABASE_PATH

DB_DIR = DATABASE_DIR
DB_PATH = DATABASE_PATH

DB_DIR.mkdir(exist_ok=True)


# --------------------------------------------------
# Database Connection
# --------------------------------------------------

def get_connection():
    """Return SQLite connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# --------------------------------------------------
# Password Utilities
# --------------------------------------------------

def hash_password(password: str) -> str:
    """Hash password using bcrypt."""
    return bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    ).decode()


def verify_password(password: str, password_hash: str) -> bool:
    """Verify password against bcrypt hash."""
    return bcrypt.checkpw(
        password.encode(),
        password_hash.encode()
    )


# --------------------------------------------------
# Database Initialization
# --------------------------------------------------

def initialize_database():
    """Create all required tables."""

    conn = get_connection()
    cursor = conn.cursor()

    # ---------------- USERS ---------------- #

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL,
            status TEXT NOT NULL,
            created_at TEXT NOT NULL,
            last_login TEXT
        )
    """)

    # ---------------- ACTIVITY LOG ---------------- #

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS activity_logs(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            action TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)

    # ---------------- PREDICTIONS ---------------- #

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            customer_id TEXT,
            prediction TEXT,
            probability REAL,
            created_at TEXT NOT NULL
        )
    """)

    conn.commit()

    # Create default admin if it doesn't exist

    cursor.execute(
        "SELECT * FROM users WHERE username=?",
        ("admin",)
    )

    admin = cursor.fetchone()

    if admin is None:

        cursor.execute("""
            INSERT INTO users(
                username,
                password_hash,
                role,
                status,
                created_at
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            "admin",
            hash_password("Admin@123"),
            "Admin",
            "Active",
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))

        conn.commit()

    conn.close()


# --------------------------------------------------
# User Management
# --------------------------------------------------

def create_user(username: str,
                password: str,
                role: str):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            INSERT INTO users(
                username,
                password_hash,
                role,
                status,
                created_at
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            username,
            hash_password(password),
            role,
            "Active",
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))

        conn.commit()

        log_activity(
            username,
            "Account Created"
        )

        return True

    except sqlite3.IntegrityError:

        return False

    finally:

        conn.close()


def authenticate_user(username: str,
                      password: str):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username=?",
        (username,)
    )

    user = cursor.fetchone()

    if user is None:
        conn.close()
        return None

    if user["status"] != "Active":
        conn.close()
        return None

    if verify_password(
            password,
            user["password_hash"]):

        cursor.execute("""
            UPDATE users
            SET last_login=?
            WHERE username=?
        """, (
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            username
        ))

        conn.commit()

        log_activity(
            username,
            "Logged In"
        )

        conn.close()

        return dict(user)

    conn.close()

    return None


def get_all_users():

    conn = get_connection()

    users = conn.execute("""
        SELECT
            username,
            role,
            status,
            created_at,
            last_login
        FROM users
    """).fetchall()

    conn.close()

    return users


def update_status(username: str,
                  status: str):

    conn = get_connection()

    conn.execute("""
        UPDATE users
        SET status=?
        WHERE username=?
    """, (
        status,
        username
    ))

    conn.commit()

    conn.close()


def reset_password(username: str,
                   new_password: str):

    conn = get_connection()

    conn.execute("""
        UPDATE users
        SET password_hash=?
        WHERE username=?
    """, (
        hash_password(new_password),
        username
    ))

    conn.commit()

    conn.close()


# --------------------------------------------------
# Activity Log
# --------------------------------------------------

def log_activity(username: str,
                 action: str):

    conn = get_connection()

    conn.execute("""
        INSERT INTO activity_logs(
            username,
            action,
            timestamp
        )
        VALUES (?, ?, ?)
    """, (
        username,
        action,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()

    conn.close()


# --------------------------------------------------
# Prediction Log
# --------------------------------------------------

def save_prediction(username: str,
                    customer_id: str,
                    prediction: str,
                    probability: float):

    conn = get_connection()

    conn.execute("""
        INSERT INTO predictions(
            username,
            customer_id,
            prediction,
            probability,
            created_at
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        username,
        customer_id,
        prediction,
        probability,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()

    conn.close()
    
"""
==========================================================
ChurnGuard
Database Manager
==========================================================
"""

# ---------------------------------------------------------
# Database Path
# ---------------------------------------------------------

DB_PATH = (
    Path(__file__).parent.parent
    / "database"
    / "users.db"
)


def get_connection():
    """
    Returns a SQLite connection with dictionary-style rows.
    """

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    return conn


def execute_query(query, params=()):
    """
    Execute INSERT/UPDATE/DELETE queries.
    """

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(query, params)

    conn.commit()

    conn.close()


def fetch_one(query, params=()):
    """
    Fetch a single row.
    """

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(query, params)

    row = cursor.fetchone()

    conn.close()

    return row


def fetch_all(query, params=()):
    """
    Fetch multiple rows.
    """

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(query, params)

    rows = cursor.fetchall()

    conn.close()

    return rows