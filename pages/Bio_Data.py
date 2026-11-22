import streamlit as st
from datetime import date

from database import save_biodata
from theme import set_background, require_login


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Bio Data",
    page_icon="👤",
    layout="wide"
)

set_background("images/bio_data_background.png")

require_login()


# ============================================================
# SESSION
# ============================================================

username = st.session_state.get(
    "username",
    ""
)


# ============================================================
# HEADER
# ============================================================

st.title("👤 Your Financial Profile")

st.caption(
    "Tell us a little about yourself so we can personalize "
    "your financial tracking and predictions."
)

st.divider()


# ============================================================
# PERSONAL INFORMATION
# ============================================================

st.subheader("👤 Personal Information")

col1, col2 = st.columns(2)

with col1:

    full_name = st.text_input(
        "Full Name",
        placeholder="Enter your full name"
    )

    email = st.text_input(
        "Email",
        placeholder="Enter your email"
    )

with col2:

    phone = st.text_input(
        "Phone Number",
        placeholder="Enter your phone number"
    )

    gender = st.selectbox(
        "Gender",
        [
            "Select",
            "Female",
            "Male",
            "Other"
        ]
    )


# ============================================================
# DATE OF BIRTH
# ============================================================

st.subheader("🎂 Date of Birth")

dob = st.date_input(
    "Select your date of birth",
    value=date(2000, 1, 1),
    min_value=date(1900, 1, 1),
    max_value=date.today()
)


# ============================================================
# EDUCATION & OCCUPATION
# ============================================================

st.subheader("🎓 Education & Career")

col3, col4 = st.columns(2)

with col3:

    education = st.text_input(
        "Education",
        placeholder="Example: B.Tech, B.Com, MBA"
    )

with col4:

    occupation = st.text_input(
        "Occupation",
        placeholder="Example: Student, Developer, Teacher"
    )


# ============================================================
# FINANCIAL INFORMATION
# ============================================================

st.subheader("💰 Financial Information")

salary = st.number_input(
    "Monthly Salary",
    min_value=0.0,
    step=1000.0,
    help="Enter your approximate monthly income."
)

financial_goal = st.text_input(
    "Financial Goal",
    placeholder="Example: Buy a car, higher savings, education..."
)


# ============================================================
# ADDRESS
# ============================================================

st.subheader("📍 Address")

address = st.text_area(
    "Address",
    placeholder="Enter your address",
    height=100
)


# ============================================================
# FINANCIAL FLOW PREVIEW
# ============================================================

st.divider()

st.subheader("💡 Your Money Journey")

flow_col1, flow_col2, flow_col3, flow_col4, flow_col5 = st.columns(5)

with flow_col1:
    st.metric(
        "Income",
        "💰"
    )

with flow_col2:
    st.metric(
        "Expenses",
        "💸"
    )

with flow_col3:
    st.metric(
        "Savings",
        "🏦"
    )

with flow_col4:
    st.metric(
        "Prediction",
        "🤖"
    )

with flow_col5:
    st.metric(
        "Goals",
        "🎯"
    )


# ============================================================
# SAVE BIO DATA
# ============================================================

st.divider()

if st.button(
    "💾 Save Bio Data & Continue",
    use_container_width=True
):

    if not full_name:

        st.warning(
            "Please enter your full name."
        )

    elif not email:

        st.warning(
            "Please enter your email."
        )

    else:

        save_biodata(
            username,
            full_name,
            email,
            phone,
            dob,
            gender,
            education,
            occupation,
            salary,
            address,
            financial_goal
        )

        st.success(
            "Bio Data saved successfully! 🎉"
        )

        st.switch_page(
            "pages/Dashboard.py"
        )