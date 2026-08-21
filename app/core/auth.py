"""
==========================================================
ChurnGuard
Authentication Service
==========================================================

Handles:
- Password hashing
- Password verification
- User authentication
- Last login update
"""

from datetime import datetime

import bcrypt

from core.database import execute_query, fetch_one


# ---------------------------------------------------------
# Password Utilities
# ---------------------------------------------------------

def hash_password(password: str) -> str:
    """
    Generate a bcrypt hash.
    """

    return bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")


def verify_password(password: str, password_hash: str) -> bool:
    """
    Verify a password against its bcrypt hash.
    """

    try:
        return bcrypt.checkpw(
            password.encode("utf-8"),
            password_hash.encode("utf-8"),
        )
    except Exception:
        return False


# ---------------------------------------------------------
# User Lookup
# ---------------------------------------------------------

def get_user(username: str):
    """
    Retrieve a user by username.
    """

    return fetch_one(
        """
        SELECT *
        FROM users
        WHERE username = ?
        """,
        (username,),
    )


# ---------------------------------------------------------
# Last Login
# ---------------------------------------------------------

def update_last_login(user_id: int):
    """
    Update last login timestamp.
    """

    execute_query(
        """
        UPDATE users
        SET last_login = ?
        WHERE id = ?
        """,
        (
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            user_id,
        ),
    )


# ---------------------------------------------------------
# Authentication
# ---------------------------------------------------------

def authenticate(username: str, password: str):
    """
    Authenticate user.

    Returns
    -------
    sqlite3.Row | None
    """

    user = get_user(username)

    if user is None:
        return None

    # Reject inactive / locked accounts
    if user["status"] != "Active":
        return None

    if not verify_password(password, user["password_hash"]):
        return None

    update_last_login(user["id"])

    return user


# ---------------------------------------------------------
# Admin Password Reset
# ---------------------------------------------------------

def reset_admin_password(new_password: str):
    """
    Reset the admin password.
    """

    execute_query(
        """
        UPDATE users
        SET password_hash = ?
        WHERE username = 'admin'
        """,
        (
            hash_password(new_password),
        ),
    )