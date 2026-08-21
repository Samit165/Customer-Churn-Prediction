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

# pyrefly: ignore [missing-import]
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


def execute_query(query, params=()):
    """Execute INSERT/UPDATE/DELETE queries."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    conn.close()


def fetch_one(query, params=()):
    """Fetch a single row."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    row = cursor.fetchone()
    conn.close()
    return row


def fetch_all(query, params=()):
    """Fetch multiple rows."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return rows


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
            full_name TEXT NOT NULL DEFAULT '',
            email TEXT,
            role TEXT NOT NULL,
            last_login TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT NOT NULL DEFAULT 'Active'
        )
    """)

    # --------------------------------------------------
    # Migrate existing users table
    # --------------------------------------------------

    cursor.execute("PRAGMA table_info(users)")

    user_columns = [
        column[1]
        for column in cursor.fetchall()
    ]

    if "status" not in user_columns:
        cursor.execute("""
            ALTER TABLE users
            ADD COLUMN status TEXT NOT NULL DEFAULT 'Active'
        """)

    if "last_login" not in user_columns:
        cursor.execute("""
            ALTER TABLE users
            ADD COLUMN last_login TEXT
        """)

    if "full_name" not in user_columns:
        cursor.execute("""
            ALTER TABLE users
            ADD COLUMN full_name TEXT NOT NULL DEFAULT ''
        """)

    if "email" not in user_columns:
        cursor.execute("""
            ALTER TABLE users
            ADD COLUMN email TEXT
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
            prediction_type TEXT NOT NULL DEFAULT 'Single',
            created_at TEXT NOT NULL
        )
    """)
    # Add prediction_type to existing databases
    cursor.execute("PRAGMA table_info(predictions)")
    prediction_columns = [
        column[1]
        for column in cursor.fetchall()
    ]

    if "prediction_type" not in prediction_columns:
        cursor.execute("""
            ALTER TABLE predictions
            ADD COLUMN prediction_type TEXT NOT NULL DEFAULT 'Single'
        """)
    

    conn.commit()

    # --------------------------------------------------
    # Admin Account Migration / Initialization
    # --------------------------------------------------

    # Check for existing admin account
    cursor.execute(
        "SELECT id FROM users WHERE username=?",
        ("admin",)
    )

    old_admin = cursor.fetchone()

    # Check whether the new admin account already exists
    cursor.execute(
        "SELECT id FROM users WHERE username=?",
        ("samit",)
    )

    new_admin = cursor.fetchone()


    # --------------------------------------------------
    # Migrate existing admin account
    # --------------------------------------------------

    if old_admin is not None and new_admin is None:

        cursor.execute("""
            UPDATE users
            SET
                username=?,
                password_hash=?,
                role=?,
                status=?
            WHERE username=?
        """, (
            "samit",
            hash_password("samit@0616"),
            "Admin",
            "Active",
            "admin"
        ))

        conn.commit()


    # --------------------------------------------------
    # Create new admin if no admin account exists
    # --------------------------------------------------

    elif old_admin is None and new_admin is None:

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
            "samit",
            hash_password("samit@0616"),
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
                role: str,
                full_name: str = "",
                email: str = ""):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        # ---------------------------------------------
        # Check whether username already exists
        # ---------------------------------------------

        cursor.execute(
            """
            SELECT id
            FROM users
            WHERE LOWER(username) = LOWER(?)
            """,
            (username.strip(),)
        )

        existing_user = cursor.fetchone()

        if existing_user is not None:

            return {
                "success": False,
                "error": "exists"
            }

        # ---------------------------------------------
        # Create user
        # ---------------------------------------------

        cursor.execute("""
            INSERT INTO users(
                username,
                password_hash,
                full_name,
                email,
                role,
                status,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            username.strip(),
            hash_password(password),
            full_name.strip() if full_name else "",
            email.strip() if email else "",
            role,
            "Active",
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))

        conn.commit()

        return {
            "success": True,
            "error": None
        }

    except sqlite3.IntegrityError as e:

        print(
            f"[DATABASE] User creation failed: {e}"
        )

        return {
            "success": False,
            "error": str(e)
        }

    except Exception as e:

        print(
            f"[DATABASE] Unexpected error creating user: {e}"
        )

        return {
            "success": False,
            "error": str(e)
        }

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
            full_name,
            email,
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

def save_prediction(
    username: str,
    customer_id: str,
    prediction: str,
    probability: float,
    prediction_type: str = "Single"
):
    """Save a single customer churn prediction."""

    conn = get_connection()

    conn.execute("""
        INSERT INTO predictions(
            username,
            customer_id,
            prediction,
            probability,
            prediction_type,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        username,
        customer_id,
        prediction,
        probability,
        prediction_type,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()


def save_predictions_bulk(records: list):
    """
    Save multiple customer churn predictions in a single transaction.

    records: list of tuples (username, customer_id, prediction, probability, prediction_type, created_at)
             or dicts with corresponding keys.
    """
    if not records:
        return

    conn = get_connection()
    cursor = conn.cursor()

    # Normalize records if tuples or dicts
    formatted = []
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for r in records:
        if isinstance(r, (list, tuple)):
            # If created_at not provided (length 5), append now_str
            if len(r) == 5:
                formatted.append((*r, now_str))
            else:
                formatted.append(r)
        elif isinstance(r, dict):
            formatted.append((
                r["username"],
                r["customer_id"],
                r["prediction"],
                r["probability"],
                r.get("prediction_type", "Bulk"),
                r.get("created_at", now_str),
            ))

    cursor.executemany("""
        INSERT INTO predictions(
            username,
            customer_id,
            prediction,
            probability,
            prediction_type,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, formatted)

    conn.commit()
    conn.close()


def delete_prediction(prediction_id: int):
    """Delete a single prediction record."""

    conn = get_connection()

    conn.execute(
        "DELETE FROM predictions WHERE id=?",
        (prediction_id,)
    )

    conn.commit()
    conn.close()


def clear_prediction_history():
    """Delete all prediction history and reset the ID sequence."""

    conn = get_connection()

    conn.execute(
        "DELETE FROM predictions"
    )
    # Reset AUTOINCREMENT sequence
    conn.execute(
        "DELETE FROM sqlite_sequence WHERE name='predictions'"
    )

    conn.commit()
    conn.close()