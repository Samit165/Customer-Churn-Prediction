# pyrefly: ignore [missing-import]
import streamlit as st

from components.metric_card import metric_card
from components.charts import (
    churn_pie,
    prediction_trend,
    model_performance
)


# ── Reusable hover-section CSS injector ──────────────────────────
def _inject_section_hover_css():
    """Inject once: shared hover styles for dashboard section cards."""
    st.markdown(
        """
        <style>
            /* ── Dashboard section cards ─────────────────── */
            .dash-section {
                background: rgba(30, 41, 59, 0.85);
                backdrop-filter: blur(12px);
                -webkit-backdrop-filter: blur(12px);
                border: 1px solid rgba(255, 255, 255, 0.06);
                border-radius: 18px;
                padding: 28px 24px;
                margin-bottom: 18px;
                position: relative;
                overflow: hidden;
                transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            }
            .dash-section::after {
                content: '';
                position: absolute;
                inset: 0;
                border-radius: 18px;
                background: linear-gradient(
                    135deg,
                    rgba(37, 99, 235, 0) 0%,
                    rgba(37, 99, 235, 0.04) 50%,
                    rgba(37, 99, 235, 0) 100%
                );
                opacity: 0;
                transition: opacity 0.4s ease;
                pointer-events: none;
            }
            .dash-section:hover {
                transform: translateY(-5px);
                border-color: rgba(96, 165, 250, 0.30);
                box-shadow:
                    0 14px 40px rgba(0, 0, 0, 0.40),
                    0 0 25px rgba(37, 99, 235, 0.15),
                    0 0 50px rgba(37, 99, 235, 0.08);
            }
            .dash-section:hover::after {
                opacity: 1;
            }

            /* ── Section header styling ──────────────────── */
            .dash-section-title {
                font-size: 20px;
                font-weight: 600;
                color: #E2E8F0;
                margin-bottom: 14px;
                display: flex;
                align-items: center;
                gap: 10px;
                transition: all 0.35s ease;
            }
            .dash-section:hover .dash-section-title {
                color: #FFFFFF;
                text-shadow: 0 0 12px rgba(96, 165, 250, 0.40);
            }
            .dash-section-title .sec-icon {
                display: inline-block;
                transition: transform 0.35s cubic-bezier(0.4, 0, 0.2, 1);
            }
            .dash-section:hover .dash-section-title .sec-icon {
                transform: scale(1.20) rotate(-8deg);
            }

            /* ── Activity table hover rows ───────────────── */
            .activity-row {
                display: flex;
                align-items: center;
                gap: 14px;
                padding: 13px 16px;
                border-radius: 12px;
                background: rgba(15, 23, 42, 0.60);
                border: 1px solid rgba(255, 255, 255, 0.04);
                margin-bottom: 8px;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                cursor: default;
            }
            .activity-row:hover {
                background: rgba(37, 99, 235, 0.12);
                border-color: rgba(96, 165, 250, 0.25);
                transform: translateX(6px);
                box-shadow: 0 4px 18px rgba(37, 99, 235, 0.18);
            }
            .activity-row:hover .act-time {
                color: #60A5FA;
            }
            .activity-row:hover .act-text {
                color: #FFFFFF;
            }
            .act-time {
                font-size: 13px;
                font-weight: 600;
                color: #64748B;
                min-width: 52px;
                transition: color 0.3s ease;
            }
            .act-dot {
                width: 7px; height: 7px;
                border-radius: 50%;
                background: #2563EB;
                flex-shrink: 0;
                box-shadow: 0 0 6px rgba(37, 99, 235, 0.50);
            }
            .act-text {
                font-size: 14px;
                color: #CBD5E1;
                transition: color 0.3s ease;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render():

    # Inject hover CSS once
    _inject_section_hover_css()

    st.title("📊 Dashboard")

    st.caption("Customer Churn Analytics Overview")

    st.info("💡 Quick Navigation: Select **🔮 Predict** from the left sidebar menu to evaluate customer churn risk.")

    # ── KPI Metric Cards ───────────────────────────────
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        metric_card(
            "Total Users",
            "254",
            "👤",
            "#3B82F6"
        )

    with c2:
        metric_card(
            "Predictions",
            "1,348",
            "🔮",
            "#10B981"
        )

    with c3:
        metric_card(
            "Churn Rate",
            "26.5%",
            "⚠️",
            "#F59E0B"
        )

    with c4:
        metric_card(
            "Accuracy",
            "85.7%",
            "🎯",
            "#8B5CF6"
        )

    st.divider()

    # ── Charts Row ─────────────────────────────────────
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown(
            '<div class="dash-section">'
            '<div class="dash-section-title"><span class="sec-icon">📈</span> Prediction Trend</div>',
            unsafe_allow_html=True,
        )
        st.plotly_chart(
            prediction_trend(),
            use_container_width=True
        )
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown(
            '<div class="dash-section">'
            '<div class="dash-section-title"><span class="sec-icon">🍩</span> Churn Distribution</div>',
            unsafe_allow_html=True,
        )
        st.plotly_chart(
            churn_pie(),
            use_container_width=True
        )
        st.markdown('</div>', unsafe_allow_html=True)

    st.divider()

    # ── Model Performance ──────────────────────────────
    st.markdown(
        '<div class="dash-section">'
        '<div class="dash-section-title"><span class="sec-icon">🏆</span> Model Performance</div>',
        unsafe_allow_html=True,
    )
    st.plotly_chart(
        model_performance(),
        use_container_width=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.divider()

    # ── Recent Activity ────────────────────────────────
    st.markdown(
        '<div class="dash-section">'
        '<div class="dash-section-title"><span class="sec-icon">🕑</span> Recent Activity</div>',
        unsafe_allow_html=True,
    )

    activities = [
        ("10:15", "✅ Prediction Completed"),
        ("09:52", "🔐 Admin Login"),
        ("09:30", "📦 Bulk Prediction"),
        ("09:05", "📄 Report Generated"),
    ]
    for time_str, desc in activities:
        st.markdown(
            f'<div class="activity-row">'
            f'  <span class="act-time">{time_str}</span>'
            f'  <span class="act-dot"></span>'
            f'  <span class="act-text">{desc}</span>'
            f'</div>',
            unsafe_allow_html=True,
        )

    st.markdown('</div>', unsafe_allow_html=True)
