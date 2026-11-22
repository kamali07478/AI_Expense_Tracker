import streamlit as st
from datetime import date

from database import add_expense
from theme import set_background, require_login


st.set_page_config(
    page_title="Add Expense",
    page_icon="💸",
    layout="wide"
)

set_background("images/add_expense_background.png")

# -----------------------------
# LOGIN CHECK
# -----------------------------

require_login()

username = st.session_state.get("username", "")


# -----------------------------
# Header
# -----------------------------

st.title("💸 Add Expense")
st.caption("TRACK EVERY EXPENSE • UNDERSTAND YOUR MONEY FLOW")
st.divider()


# -----------------------------
# Money Flow
# -----------------------------

flow = [
    ("💰", "Income"),
    ("💸", "Expenses"),
    ("🏦", "Savings"),
    ("📊", "Analysis"),
    ("🤖", "Prediction"),
    ("🎯", "Goals")
]

flow_cols = st.columns(6)

for col, (icon, label) in zip(flow_cols, flow):

    with col:

        st.markdown(f"### {icon}")
        st.caption(label)


st.divider()


# -----------------------------
# Expense Form
# -----------------------------

st.subheader("📝 Expense Details")

st.caption(
    "Record your spending so your AI tracker can understand your financial habits."
)

col1, col2 = st.columns(2, gap="large")

with col1:

    expense_date = st.date_input(
        "📅 Expense Date",
        value=date.today()
    )

    category = st.selectbox(
        "🏷️ Expense Category",
        [
            "Food",
            "Travel",
            "Shopping",
            "Education",
            "Bills",
            "Health",
            "Entertainment",
            "Other"
        ]
    )

with col2:

    amount = st.number_input(
        "💰 Expense Amount",
        min_value=0.0,
        step=100.0,
        format="%.2f"
    )

    description = st.text_area(
        "📝 Description",
        placeholder="Example: Lunch, bus ticket, college books...",
        height=120
    )


st.divider()


# -----------------------------
# Expense Preview
# -----------------------------

st.subheader("👀 Expense Preview")

preview_col1, preview_col2, preview_col3 = st.columns(3)

with preview_col1:

    st.metric(
        "Category",
        category
    )

with preview_col2:

    st.metric(
        "Amount",
        f"₹{amount:,.2f}"
    )

with preview_col3:

    st.metric(
        "Date",
        expense_date.strftime("%d %b %Y")
    )


st.divider()


# -----------------------------
# Save Expense
# -----------------------------

if st.button(
    "💸 Add Expense",
    use_container_width=True
):

    if amount <= 0:

        st.warning(
            "Please enter a valid expense amount."
        )

    else:

        add_expense(
            username,
            expense_date,
            category,
            amount,
            description
        )

        st.success(
            "Expense added successfully! 🎉"
        )

        st.balloons()