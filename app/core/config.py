"""
config.py
---------------------------------------
Central configuration for ChurnGuard.

This file stores:
- Application information
- User roles
- Account status
- Database settings
- Model paths
- Theme colors
"""

from pathlib import Path

# ==========================================================
# APPLICATION INFORMATION
# ==========================================================

APP_NAME = "ChurnGuard"

APP_VERSION = "1.0.0"

APP_TAGLINE = "Enterprise Customer Retention Intelligence Platform"

APP_DESCRIPTION = (
    "AI-powered customer churn prediction system "
    "using XGBoost and SHAP Explainability."
)

# ==========================================================
# PROJECT PATHS
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

PROJECT_ROOT = BASE_DIR.parent

DATABASE_DIR = BASE_DIR / "database"

MODEL_DIR = PROJECT_ROOT / "models"

ASSETS_DIR = BASE_DIR / "assets"

CSS_DIR = ASSETS_DIR / "css"

IMAGE_DIR = ASSETS_DIR / "images"

ICON_DIR = ASSETS_DIR / "icons"

LOTTIE_DIR = ASSETS_DIR / "lottie"

# ==========================================================
# DATABASE
# ==========================================================

DATABASE_NAME = "users.db"

DATABASE_PATH = DATABASE_DIR / DATABASE_NAME

# ==========================================================
# MODEL FILES
# ==========================================================

MODEL_PATH = MODEL_DIR / "churn_model.pkl"

PREPROCESSOR_PATH = MODEL_DIR / "preprocessor.pkl"

# ==========================================================
# USER ROLES
# ==========================================================

ROLES = {
    "ADMIN": "Admin",
    "MANAGER": "Manager",
    "EMPLOYEE": "Employee"
}

# ==========================================================
# ACCOUNT STATUS
# ==========================================================

STATUS = {
    "ACTIVE": "Active",
    "INACTIVE": "Inactive",
    "LOCKED": "Locked"
}

# ==========================================================
# SESSION KEYS
# ==========================================================

SESSION = {
    "LOGGED_IN": "logged_in",
    "USERNAME": "username",
    "ROLE": "role"
}

# ==========================================================
# THEME COLORS
# ==========================================================

COLORS = {
    "PRIMARY": "#2563EB",
    "SUCCESS": "#22C55E",
    "WARNING": "#F59E0B",
    "DANGER": "#EF4444",
    "BACKGROUND": "#0F172A",
    "CARD": "#1E293B",
    "TEXT": "#F8FAFC"
}

# ==========================================================
# SUPPORTED FILE TYPES
# ==========================================================

ALLOWED_UPLOAD_TYPES = [
    "csv"
]