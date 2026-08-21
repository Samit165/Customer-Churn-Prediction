# pyrefly: ignore [missing-import]

import streamlit as st
import pandas as pd

from core.database import (
    get_all_users,
    create_user,
    update_status,
    reset_password,
    fetch_all,
    log_activity,
)


# --------------------------------------------------
# Admin UI Styling
# --------------------------------------------------

def _inject_admin_css():
    """Inject Admin page-specific styling."""

    st.markdown(
        """
        <style>

        /* ---------------------------------------------
           Admin section cards
        --------------------------------------------- */

        .admin-section {
            background: rgba(30, 41, 59, 0.82);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-radius: 18px;
            padding: 24px;
            margin-bottom: 20px;
            transition: all 0.35s ease;
        }

        .admin-section:hover {
            border-color: rgba(96, 165, 250, 0.25);
            box-shadow:
                0 12px 35px rgba(0, 0, 0, 0.30),
                0 0 25px rgba(37, 99, 235, 0.08);
        }

        .admin-section-title {
            font-size: 20px;
            font-weight: 600;
            color: #E2E8F0;
            margin-bottom: 6px;
        }

        .admin-section-caption {
            color: #64748B;
            font-size: 13px;
            margin-bottom: 18px;
        }

        /* ---------------------------------------------
           Status badges
        --------------------------------------------- */

        .admin-badge-active {
            display: inline-block;
            padding: 4px 10px;
            border-radius: 999px;
            background: rgba(16, 185, 129, 0.12);
            color: #34D399;
            border: 1px solid rgba(16, 185, 129, 0.20);
            font-size: 12px;
            font-weight: 600;
        }

        .admin-badge-inactive {
            display: inline-block;
            padding: 4px 10px;
            border-radius: 999px;
            background: rgba(239, 68, 68, 0.12);
            color: #F87171;
            border: 1px solid rgba(239, 68, 68, 0.20);
            font-size: 12px;
            font-weight: 600;
        }

        .admin-badge-role {
            display: inline-block;
            padding: 4px 10px;
            border-radius: 999px;
            background: rgba(59, 130, 246, 0.12);
            color: #60A5FA;
            border: 1px solid rgba(59, 130, 246, 0.20);
            font-size: 12px;
            font-weight: 600;
        }

        /* ---------------------------------------------
           Activity rows
        --------------------------------------------- */

        .admin-activity-row {
            display: flex;
            align-items: center;
            gap: 14px;
            padding: 12px 14px;
            margin-bottom: 8px;
            border-radius: 12px;
            background: rgba(15, 23, 42, 0.55);
            border: 1px solid rgba(255, 255, 255, 0.04);
            transition: all 0.25s ease;
        }

        .admin-activity-row:hover {
            background: rgba(37, 99, 235, 0.10);
            border-color: rgba(96, 165, 250, 0.20);
            transform: translateX(4px);
        }

        .admin-activity-dot {
            width: 7px;
            height: 7px;
            border-radius: 50%;
            background: #2563EB;
            box-shadow: 0 0 7px rgba(37, 99, 235, 0.55);
            flex-shrink: 0;
        }

        .admin-activity-user {
            min-width: 90px;
            color: #64748B;
            font-size: 12px;
            font-weight: 600;
        }

        .admin-activity-action {
            flex: 1;
            color: #CBD5E1;
            font-size: 13px;
        }

        .admin-activity-time {
            color: #475569;
            font-size: 11px;
            white-space: nowrap;
        }

        /* ---------------------------------------------
           System information
        --------------------------------------------- */

        .system-info {
            padding: 12px 0;
            border-bottom: 1px solid rgba(255,255,255,0.05);
        }

        .system-info:last-child {
            border-bottom: none;
        }

        .system-info-label {
            color: #64748B;
            font-size: 12px;
        }

        .system-info-value {
            color: #E2E8F0;
            font-size: 14px;
            font-weight: 600;
            margin-top: 3px;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )


# --------------------------------------------------
# Helpers
# --------------------------------------------------

def _get_current_user():
    """Return the currently authenticated user."""

    user = st.session_state.get("user")

    if isinstance(user, dict):
        return user

    return {}


def _load_users():
    """Load all users into a DataFrame."""

    rows = get_all_users()

    if not rows:
        return pd.DataFrame(
            columns=[
                "username",
                "role",
                "status",
                "created_at",
                "last_login",
            ]
        )

    return pd.DataFrame(
        [dict(row) for row in rows]
    )


def _load_activity():
    """Load recent system activity."""

    return fetch_all("""
        SELECT
            username,
            action,
            timestamp
        FROM activity_logs
        ORDER BY id DESC
        LIMIT 15
    """)


def _load_system_counts():
    """Load system-wide counts."""

    total_users = fetch_all(
        "SELECT COUNT(*) AS count FROM users"
    )[0]["count"]

    active_users = fetch_all(
        "SELECT COUNT(*) AS count FROM users WHERE status='Active'"
    )[0]["count"]

    inactive_users = fetch_all(
        "SELECT COUNT(*) AS count FROM users WHERE status!='Active'"
    )[0]["count"]

    admin_users = fetch_all(
        "SELECT COUNT(*) AS count FROM users WHERE role='Admin'"
    )[0]["count"]

    total_predictions = fetch_all(
        "SELECT COUNT(*) AS count FROM predictions"
    )[0]["count"]

    total_activity = fetch_all(
        "SELECT COUNT(*) AS count FROM activity_logs"
    )[0]["count"]

    return (
        total_users,
        active_users,
        inactive_users,
        admin_users,
        total_predictions,
        total_activity,
    )


# --------------------------------------------------
# Main Admin Page
# --------------------------------------------------

def render():

    _inject_admin_css()

    # --------------------------------------------------
    # Authorization
    # --------------------------------------------------

    user = _get_current_user()

    if user.get("role") != "Admin":

        st.error("🚫 Access Denied")

        st.warning(
            "You do not have administrator privileges "
            "to access this section."
        )

        return

    username = user.get(
        "username",
        "Admin"
    )

    # --------------------------------------------------
    # Header
    # --------------------------------------------------

    st.title("🛡️ Admin Console")

    st.caption(
        "System administration, user management, and activity monitoring."
    )

    st.success(
        f"🔐 Administrator session active — **{username}**"
    )

    # --------------------------------------------------
    # System Overview
    # --------------------------------------------------

    st.subheader("📊 System Overview")

    (
        total_users,
        active_users,
        inactive_users,
        admin_users,
        total_predictions,
        total_activity,
    ) = _load_system_counts()

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "👥 Total Users",
            total_users
        )

    with c2:
        st.metric(
            "🟢 Active Users",
            active_users
        )

    with c3:
        st.metric(
            "🔴 Inactive Users",
            inactive_users
        )

    with c4:
        st.metric(
            "🛡️ Admin Accounts",
            admin_users
        )

    c5, c6 = st.columns(2)

    with c5:
        st.metric(
            "🔮 Total Predictions",
            total_predictions
        )

    with c6:
        st.metric(
            "🕒 Activity Records",
            total_activity
        )

    st.divider()

    # --------------------------------------------------
    # User Management
    # --------------------------------------------------

    st.subheader("👥 User Management")

    users_df = _load_users()

    if users_df.empty:

        st.info("No users found.")

    else:

        search = st.text_input(
            "🔍 Search Users",
            placeholder="Search by username or role..."
        )

        filtered_users = users_df.copy()

        if search.strip():

            search_value = search.strip().lower()

            filtered_users = filtered_users[
                filtered_users["username"]
                .str.lower()
                .str.contains(
                    search_value,
                    na=False
                )
                |
                filtered_users["role"]
                .str.lower()
                .str.contains(
                    search_value,
                    na=False
                )
            ]

        display_df = filtered_users.copy()

        display_df["status"] = (
            display_df["status"]
            .map({
                "Active": "🟢 Active",
                "Inactive": "🔴 Inactive"
            })
            .fillna(display_df["status"])
        )

        display_df["role"] = (
            display_df["role"]
            .map({
                "Admin": "🛡️ Admin",
                "User": "👤 User"
            })
            .fillna(display_df["role"])
        )

        display_df = display_df.rename(
            columns={
                "username": "Username",
                "role": "Role",
                "status": "Status",
                "created_at": "Created",
                "last_login": "Last Login",
            }
        )

        st.dataframe(
            display_df[
                [
                    "Username",
                    "Role",
                    "Status",
                    "Created",
                    "Last Login",
                ]
            ],
            use_container_width=True,
            hide_index=True,
        )

        st.caption(
            f"Showing {len(filtered_users)} of "
            f"{len(users_df)} users."
        )

    # --------------------------------------------------
    # User Actions
    # --------------------------------------------------

    st.markdown("### ⚙️ User Actions")

    action_col1, action_col2 = st.columns(2)

    # --------------------------------------------------
    # Account Status
    # --------------------------------------------------

    with action_col1:

        st.markdown("#### 🔄 Account Status")

        if users_df.empty:

            st.info("No users available.")

        else:

            status_user = st.selectbox(
                "Select User",
                users_df["username"].tolist(),
                key="status_user"
            )

            selected_user_row = users_df[
                users_df["username"] == status_user
            ]

            if not selected_user_row.empty:

                current_status = selected_user_row.iloc[0]["status"]

                st.caption(
                    f"Current status: **{current_status}**"
                )

            # Protect current administrator
            if status_user == username:

                st.warning(
                    "You cannot disable your own administrator account."
                )

            else:

                new_status = (
                    "Inactive"
                    if current_status == "Active"
                    else "Active"
                )

                button_label = (
                    "🔴 Disable Account"
                    if current_status == "Active"
                    else "🟢 Activate Account"
                )

                if st.button(
                    button_label,
                    use_container_width=True,
                    key="change_status"
                ):

                    update_status(
                        status_user,
                        new_status
                    )

                    log_activity(
                        username,
                        f"Changed {status_user} status to {new_status}"
                    )

                    st.success(
                        f"{status_user} is now {new_status}."
                    )

                    st.rerun()

    # --------------------------------------------------
    # Password Reset
    # --------------------------------------------------

    with action_col2:

        st.markdown("#### 🔑 Reset Password")

        if users_df.empty:

            st.info("No users available.")

        else:

            password_user = st.selectbox(
                "Select User",
                users_df["username"].tolist(),
                key="password_user"
            )

            with st.form("reset_password_form"):

                new_password = st.text_input(
                    "New Password",
                    type="password",
                    placeholder="Enter new password"
                )

                confirm_password = st.text_input(
                    "Confirm Password",
                    type="password",
                    placeholder="Confirm new password"
                )

                reset_clicked = st.form_submit_button(
                    "🔑 Reset Password",
                    use_container_width=True
                )

                if reset_clicked:

                    if not new_password:

                        st.error(
                            "Please enter a new password."
                        )

                    elif len(new_password) < 6:

                        st.error(
                            "Password must contain at least 6 characters."
                        )

                    elif new_password != confirm_password:

                        st.error(
                            "Passwords do not match."
                        )

                    else:

                        reset_password(
                            password_user,
                            new_password
                        )

                        log_activity(
                            username,
                            f"Reset password for {password_user}"
                        )

                        st.success(
                            f"Password reset successfully for "
                            f"**{password_user}**."
                        )

    st.divider()

    # --------------------------------------------------
    # Create User
    # --------------------------------------------------

    st.subheader("➕ Create New User")

    with st.form("create_user_form"):

        col1, col2, col3 = st.columns(3)

        with col1:

            new_username = st.text_input(
                "Username",
                placeholder="Enter username"
            )

        with col2:

            new_user_password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter password"
            )

        with col3:

            new_role = st.selectbox(
                "Role",
                [
                    "User",
                    "Admin"
                ],
                index=0
            )

        create_clicked = st.form_submit_button(
            "➕ Create User",
            use_container_width=True
        )

        if create_clicked:

            clean_username = new_username.strip()

            if not clean_username:

                st.error(
                    "Username is required."
                )

            elif len(clean_username) < 3:

                st.error(
                    "Username must contain at least 3 characters."
                )

            elif not new_user_password:

                st.error(
                    "Password is required."
                )

            elif len(new_user_password) < 6:

                st.error(
                    "Password must contain at least 6 characters."
                )

            else:

                result = create_user(
                    clean_username,
                    new_user_password,
                    new_role
                )

                if result["success"]:

                    log_activity(
                        username,
                        f"Created user {clean_username}"
                    )

                    st.success(
                        f"User **{clean_username}** created successfully."
                    )

                    st.rerun()

                elif result["error"] == "exists":

                    st.error(
                        f"Username **{clean_username}** already exists."
                    )

                else:

                    st.error(
                        f"Unable to create user: {result['error']}"
                    )

    st.divider()

    # --------------------------------------------------
    # Activity Monitor
    # --------------------------------------------------

    st.subheader("🕒 Activity Monitor")

    st.caption(
        "Latest system activity across ChurnGuard."
    )

    logs = _load_activity()

    if logs:

        for row in logs:

            log_username = str(
                row["username"]
            )

            action = str(
                row["action"]
            )

            timestamp = str(
                row["timestamp"]
            )

            # Select icon based on action
            if "Login" in action:
                icon = "🔐"

            elif "Prediction" in action:
                icon = "🔮"

            elif "Bulk" in action:
                icon = "📦"

            elif "Account" in action:
                icon = "👤"

            elif "password" in action.lower():
                icon = "🔑"

            elif "status" in action.lower():
                icon = "🔄"

            else:
                icon = "🔔"

            try:
                time_part = timestamp.split(" ")[1][:5]
            except (IndexError, AttributeError):
                time_part = timestamp[:5]

            st.markdown(
                f"""
                <div class="admin-activity-row">
                    <span class="admin-activity-dot"></span>
                    <span class="admin-activity-user">
                        {log_username}
                    </span>
                    <span class="admin-activity-action">
                        {icon} {action}
                    </span>
                    <span class="admin-activity-time">
                        {time_part}
                    </span>
                </div>
                """,
                unsafe_allow_html=True
            )

    else:

        st.info(
            "No activity has been recorded yet."
        )

    st.divider()

    # --------------------------------------------------
    # System Information
    # --------------------------------------------------

    st.subheader("⚙️ System Information")

    info_col1, info_col2 = st.columns(2)

    with info_col1:

        st.markdown(
            """
            <div class="system-info">
                <div class="system-info-label">
                    Application
                </div>
                <div class="system-info-value">
                    ChurnGuard
                </div>
            </div>

            <div class="system-info">
                <div class="system-info-label">
                    Database
                </div>
                <div class="system-info-value">
                    SQLite
                </div>
            </div>

            <div class="system-info">
                <div class="system-info-label">
                    Authentication
                </div>
                <div class="system-info-value">
                    bcrypt
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with info_col2:

        st.markdown(
            f"""
            <div class="system-info">
                <div class="system-info-label">
                    Current Administrator
                </div>
                <div class="system-info-value">
                    {username}
                </div>
            </div>

            <div class="system-info">
                <div class="system-info-label">
                    Total Predictions
                </div>
                <div class="system-info-value">
                    {total_predictions}
                </div>
            </div>

            <div class="system-info">
                <div class="system-info-label">
                    Activity Records
                </div>
                <div class="system-info-value">
                    {total_activity}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )