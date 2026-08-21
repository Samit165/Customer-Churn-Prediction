# pyrefly: ignore [missing-import]
import streamlit as st
import hashlib


def metric_card(title, value, icon, color="#2563EB"):
    # Generate a unique class name per card to scope hover styles
    uid = hashlib.md5(f"{title}{value}".encode()).hexdigest()[:8]
    card_class = f"mc-{uid}"

    st.markdown(
        f"""
        <style>
            .{card_class} {{
                background: #1E293B;
                padding: 20px;
                border-radius: 16px;
                border-left: 6px solid {color};
                box-shadow: 0 4px 20px rgba(0,0,0,0.35);
                transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
                cursor: default;
                position: relative;
                overflow: hidden;
            }}
            .{card_class}::before {{
                content: '';
                position: absolute;
                top: 0; left: 0; right: 0; bottom: 0;
                background: linear-gradient(
                    135deg,
                    rgba(255,255,255,0) 0%,
                    rgba(255,255,255,0.03) 50%,
                    rgba(255,255,255,0) 100%
                );
                opacity: 0;
                transition: opacity 0.35s ease;
                pointer-events: none;
                border-radius: 16px;
            }}
            .{card_class}:hover {{
                transform: translateY(-6px) scale(1.02);
                box-shadow:
                    0 12px 35px rgba(0,0,0,0.45),
                    0 0 20px {color}33,
                    0 0 40px {color}1A;
                border-left-color: {color};
                background: #1E293B;
            }}
            .{card_class}:hover::before {{
                opacity: 1;
            }}
            .{card_class}:hover .mc-icon {{
                transform: scale(1.25) rotate(-5deg);
                filter: drop-shadow(0 0 8px {color});
            }}
            .{card_class}:hover .mc-value {{
                color: {color};
                text-shadow: 0 0 15px {color}55;
            }}
            .{card_class}:hover .mc-title {{
                color: #FFFFFF;
            }}
            .{card_class} .mc-icon {{
                transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
            }}
            .{card_class} .mc-value {{
                transition: all 0.35s ease;
            }}
            .{card_class} .mc-title {{
                transition: color 0.35s ease;
            }}
        </style>
        <div class="{card_class}">
            <div style="font-size:17px; font-weight:600; color:#CBD5E1; display:flex; align-items:center; gap:8px;">
                <span class="mc-icon" style="font-size:22px;">{icon}</span>
                <span class="mc-title">{title}</span>
            </div>
            <div class="mc-value" style="font-size:32px; font-weight:700; color:#FFFFFF; margin-top:8px;">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
