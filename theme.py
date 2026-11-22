import streamlit as st
import base64
from pathlib import Path


def set_background(image_path):

    image_file = Path(image_path)

    if image_file.exists():

        with open(image_file, "rb") as file:
            encoded = base64.b64encode(file.read()).decode()

        st.markdown(
            f"""
            <style>

            /* =========================================
               BACKGROUND
               ========================================= */

            .stApp {{
                background-image:
                    linear-gradient(
                        rgba(255, 255, 255, 0.20),
                        rgba(255, 255, 255, 0.20)
                    ),
                    url("data:image/png;base64,{encoded}");

                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }}


            /* =========================================
               MAIN PAGE
               ========================================= */

            .block-container {{
                padding-top: 2rem;
                padding-bottom: 3rem;
                max-width: 1400px;
            }}


            /* =========================================
               BOLD BLACK HEADINGS
               ========================================= */

            h1,
            h2,
            h3,
            h4,
            h5,
            h6 {{
                color: #000000 !important;
                font-weight: 900 !important;
                text-shadow: none !important;
            }}


            /* =========================================
               BOLD BLACK NORMAL TEXT
               ========================================= */

            .stMarkdown p,
            .stCaption,
            p {{
                color: #000000 !important;
                font-weight: 700 !important;
                text-shadow: none !important;
            }}


            /* =========================================
               BOLD BLACK FORM LABELS
               ========================================= */

            .stTextInput label,
            .stNumberInput label,
            .stDateInput label,
            .stSelectbox label,
            .stTextArea label {{
                color: #000000 !important;
                font-weight: 900 !important;
                text-shadow: none !important;
            }}


            /* =========================================
               INPUT BOXES
               ========================================= */

            .stTextInput input,
            .stNumberInput input,
            .stDateInput input,
            .stTextArea textarea {{
                background-color:
                    rgba(255, 255, 255, 0.96) !important;

                color: #000000 !important;

                -webkit-text-fill-color: #000000 !important;

                border:
                    2px solid rgba(20, 90, 150, 0.35)
                    !important;

                border-radius: 12px !important;

                font-weight: 700 !important;
            }}


            .stTextInput input::placeholder,
            .stTextArea textarea::placeholder {{
                color: #526b82 !important;
                opacity: 1 !important;
            }}


            /* =========================================
               SELECT BOX
               ========================================= */

            .stSelectbox > div > div {{
                background-color:
                    rgba(255, 255, 255, 0.96) !important;

                color: #000000 !important;

                border-radius: 12px !important;
            }}


            .stSelectbox [data-baseweb="select"] * {{
                color: #000000 !important;
            }}


            /* =========================================
               BUTTONS
               ========================================= */

            .stButton > button {{
                width: 100%;

                border: none;

                border-radius: 12px;

                padding: 12px 20px;

                font-weight: 800;

                color: white !important;

                background:
                    linear-gradient(
                        90deg,
                        #08aeea,
                        #4268e8,
                        #7b3ff2
                    ) !important;

                box-shadow:
                    0 7px 20px
                    rgba(40, 100, 200, 0.28);
            }}


            .stButton > button p {{
                color: white !important;
                text-shadow: none !important;
            }}


            .stButton > button:hover {{
                transform: translateY(-2px);

                box-shadow:
                    0 10px 25px
                    rgba(40, 100, 200, 0.40);
            }}


            /* =========================================
               SIDEBAR
               ========================================= */

            section[data-testid="stSidebar"] {{
                background:
                    linear-gradient(
                        180deg,
                        #123b63,
                        #082744
                    ) !important;

                border-right:
                    2px solid rgba(255, 255, 255, 0.20);
            }}


            section[data-testid="stSidebar"] > div {{
                background:
                    linear-gradient(
                        180deg,
                        #123b63,
                        #082744
                    ) !important;
            }}


            /* Sidebar words */

            section[data-testid="stSidebar"] p,
            section[data-testid="stSidebar"] span,
            section[data-testid="stSidebar"] label,
            section[data-testid="stSidebar"] div {{
                color: #ffffff !important;
            }}


            /* Sidebar buttons */

            section[data-testid="stSidebar"] button {{
                color: white !important;

                background: transparent !important;

                border-radius: 10px !important;
            }}


            section[data-testid="stSidebar"] button:hover {{
                background:
                    rgba(255, 255, 255, 0.15) !important;
            }}


            /* =========================================
               METRIC CARDS
               ========================================= */

            [data-testid="stMetric"] {{
                background:
                    rgba(255, 255, 255, 0.90) !important;

                border:
                    1px solid rgba(20, 90, 150, 0.20);

                border-radius: 18px;

                padding: 20px;

                box-shadow:
                    0 8px 25px
                    rgba(20, 70, 120, 0.15);
            }}


            [data-testid="stMetricLabel"] {{
                color: #000000 !important;
                font-weight: 800 !important;
            }}


            [data-testid="stMetricValue"] {{
                color: #000000 !important;
                font-weight: 900 !important;
            }}


            /* =========================================
               ALERTS / MESSAGES
               ========================================= */

            [data-testid="stAlert"] p {{
                color: #000000 !important;
                text-shadow: none !important;
                font-weight: 700 !important;
            }}


            /* =========================================
               DIVIDER
               ========================================= */

            hr {{
                border-color:
                    rgba(0, 0, 0, 0.25) !important;
            }}


            /* =========================================
               STREAMLIT DEFAULT UI
               ========================================= */

            #MainMenu {{
                visibility: hidden;
            }}

            footer {{
                visibility: hidden;
            }}

            header {{
                background: transparent !important;
            }}

            </style>
            """,
            unsafe_allow_html=True
        )


def require_login():

    if not st.session_state.get("logged_in", False):
        st.switch_page("app.py")