import streamlit as st

from database import (
    create_database,
    create_user,
    check_login,
    get_biodata
)

from theme import set_background


# --------------------------------------------------
# PAGE SETTINGS
# --------------------------------------------------

st.set_page_config(
    page_title="AI Expense Tracker",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# --------------------------------------------------
# LOGIN PAGE BACKGROUND
# --------------------------------------------------

set_background("images/login_background.png")


# --------------------------------------------------
# DATABASE
# --------------------------------------------------

create_database()


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("💰 AI Expense Tracker")
st.caption("TRACK • PREDICT • BUILD YOUR FUTURE")


# --------------------------------------------------
# MONEY FLOW
# --------------------------------------------------

flow = [
    ("💰", "Income"),
    ("→", ""),
    ("💸", "Expenses"),
    ("→", ""),
    ("🏦", "Savings"),
    ("→", ""),
    ("📊", "Analysis"),
    ("→", ""),
    ("🤖", "Prediction"),
    ("→", ""),
    ("🎯", "Goals")
]

columns = st.columns(11)

for i, (icon, name) in enumerate(flow):

    with columns[i]:

        if name:
            st.markdown(f"### {icon}")
            st.caption(name)
        else:
            st.markdown(f"## {icon}")


st.divider()


# --------------------------------------------------
# IF USER IS ALREADY LOGGED IN
# --------------------------------------------------

if st.session_state.logged_in:

    username = st.session_state.username

    biodata = get_biodata(username)

    # Existing user with completed Bio Data
    if biodata:
        st.switch_page("pages/Dashboard.py")

    # New user who has not completed Bio Data
    else:
        st.switch_page("pages/Bio_Data.py")


# --------------------------------------------------
# LOGIN + CREATE ACCOUNT
# --------------------------------------------------

login_col, account_col = st.columns(
    2,
    gap="large"
)


# ==================================================
# LOGIN
# ==================================================

with login_col:

    st.subheader("🔐 Welcome Back")

    st.caption(
        "Continue your financial journey."
    )

    username = st.text_input(
        "Username",
        key="login_username"
    )

    password = st.text_input(
        "Password",
        type="password",
        key="login_password"
    )


    if st.button(
        "Login",
        use_container_width=True
    ):

        username = username.strip()

        if not username or not password:

            st.warning(
                "Please enter username and password."
            )

        elif check_login(
            username,
            password
        ):

            st.session_state.logged_in = True
            st.session_state.username = username

            # Check whether Bio Data already exists
            biodata = get_biodata(username)

            if biodata:
                st.switch_page("pages/Dashboard.py")
            else:
                st.switch_page("pages/Bio_Data.py")

        else:

            st.error(
                "Invalid username or password."
            )


# ==================================================
# CREATE NEW ACCOUNT
# ==================================================

with account_col:

    st.subheader("🚀 Create Your Account")

    st.caption(
        "Start tracking, saving and predicting."
    )


    new_username = st.text_input(
        "Create Username",
        key="new_username"
    ).strip()


    new_password = st.text_input(
        "Create Password",
        type="password",
        key="new_password"
    )


    confirm_password = st.text_input(
        "Confirm Password",
        type="password",
        key="confirm_password"
    )


    if st.button(
        "Create Account",
        use_container_width=True
    ):

        if (
            not new_username
            or not new_password
            or not confirm_password
        ):

            st.warning(
                "Please fill in all fields."
            )

        elif new_password != confirm_password:

            st.error(
                "Passwords do not match."
            )

        else:

            account_created = create_user(
                new_username,
                new_password
            )


            if account_created:

                st.session_state.logged_in = True
                st.session_state.username = new_username

                # NEW ACCOUNT → BIO DATA
                st.switch_page(
                    "pages/Bio_Data.py"
                )

            else:

                st.error(
                    "Username already exists."
                )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "💰 Track your money  •  "
    "🏦 Build your savings  •  "
    "🤖 Predict your future  •  "
    "🎯 Reach your goals"
)