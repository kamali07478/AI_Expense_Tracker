from theme import set_background
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression

from database import (
    get_biodata,
    get_expenses,
    get_savings,
    get_monthly_salary,
    save_monthly_salary
)

from theme import set_background, require_login


# =========================================================
# PAGE SETTINGS
# =========================================================
st.set_page_config(
    page_title="AI Expense Tracker",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

set_background("images/dashboard_background.png")


st.markdown(
    """
    <style>
    /* General bordered Streamlit containers */
    /* White cards for every bordered dashboard section */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(255, 255, 255, 0.96) !important;
        background-color: rgba(255, 255, 255, 0.96) !important;
        border: 1px solid rgba(255, 255, 255, 0.98) !important;
        border-radius: 18px !important;
        padding: 18px 22px !important;
        margin: 10px 0 20px 0 !important;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.20) !important;
        overflow: hidden !important;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] > div {
        background: rgba(255, 255, 255, 0.96) !important;
        background-color: rgba(255, 255, 255, 0.96) !important;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] div[data-testid="stVerticalBlock"] {
        background: transparent !important;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] h1,
    div[data-testid="stVerticalBlockBorderWrapper"] h2,
    div[data-testid="stVerticalBlockBorderWrapper"] h3,
    div[data-testid="stVerticalBlockBorderWrapper"] p,
    div[data-testid="stVerticalBlockBorderWrapper"] label {
        color: #111827 !important;
    }

    /* Custom white information cards */
    .white-card {
        background: rgba(255, 255, 255, 0.97);
        border: 1px solid rgba(255, 255, 255, 0.98);
        border-radius: 18px;
        padding: 22px 26px;
        margin: 8px 0 16px 0;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.18);
        color: #111827;
    }

    .white-card h2,
    .white-card h3 {
        color: #10243a !important;
        margin: 0 0 14px 0;
        font-weight: 700;
    }

    .white-card p {
        color: #17202a !important;
        font-size: 17px;
        font-weight: 600;
        line-height: 1.55;
        margin: 8px 0;
    }

    .white-card .tip-title {
        font-size: 20px;
        font-weight: 700;
        color: #10243a !important;
        margin-bottom: 8px;
    }

    .white-card .goal-text {
        font-size: 18px;
        font-weight: 700;
        color: #17202a !important;
    }

    /* Make ALL dashboard content sit on white cards */
    div[data-testid="stMainBlockContainer"] > div,
    div[data-testid="stMainBlockContainer"] .stMarkdown,
    div[data-testid="stMainBlockContainer"] .stAlert,
    div[data-testid="stMainBlockContainer"] [data-testid="stMetric"],
    div[data-testid="stMainBlockContainer"] [data-testid="stDataFrame"],
    div[data-testid="stMainBlockContainer"] [data-testid="stPlotlyChart"] {
        color: #111827 !important;
    }

    /* Main headings and normal text get a white readable background */
    div[data-testid="stMainBlockContainer"] h1,
    div[data-testid="stMainBlockContainer"] h2,
    div[data-testid="stMainBlockContainer"] h3,
    div[data-testid="stMainBlockContainer"] p,
    div[data-testid="stMainBlockContainer"] .stCaption {
        color: #111827 !important;
    }

    /* White boxes for alerts/messages */
    div[data-testid="stMainBlockContainer"] .stAlert {
        background: rgba(255,255,255,0.96) !important;
        border: 1px solid rgba(0,0,0,0.10) !important;
        border-radius: 16px !important;
        box-shadow: 0 6px 20px rgba(0,0,0,0.14) !important;
        color: #111827 !important;
    }

    /* White metric cards */
    div[data-testid="stMainBlockContainer"] [data-testid="stMetric"] {
        background: rgba(255,255,255,0.96) !important;
        border-radius: 16px !important;
        padding: 14px !important;
        border: 1px solid rgba(0,0,0,0.10) !important;
        box-shadow: 0 6px 20px rgba(0,0,0,0.14) !important;
    }

    div[data-testid="stMainBlockContainer"] [data-testid="stMetricLabel"],
    div[data-testid="stMainBlockContainer"] [data-testid="stMetricValue"],
    div[data-testid="stMainBlockContainer"] [data-testid="stMetricDelta"] {
        color: #111827 !important;
    }

    /* White table area */
    div[data-testid="stMainBlockContainer"] [data-testid="stDataFrame"] {
        background: rgba(255,255,255,0.96) !important;
        border-radius: 16px !important;
        padding: 8px !important;
        box-shadow: 0 6px 20px rgba(0,0,0,0.14) !important;
    }

    /* White chart cards */
    div[data-testid="stMainBlockContainer"] [data-testid="stPlotlyChart"] {
        background: rgba(255,255,255,0.96) !important;
        border-radius: 16px !important;
        padding: 8px !important;
        box-shadow: 0 6px 20px rgba(0,0,0,0.14) !important;
    }

    /* White page-level cards around normal sections */
    div[data-testid="stMainBlockContainer"] > div[data-testid="stVerticalBlock"] {
        border-radius: 18px;
    }

    /* Keep the dashboard readable over the background image */
    .stMarkdown, .stCaption, .stText {
        text-shadow: none !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# Allow access only after login
require_login()


# =========================================================
# LOGIN CHECK
# =========================================================

username = st.session_state.get("username", "")

if not username:
    st.warning("Please login first.")
    st.stop()


# =========================================================
# GET BIO DATA
# =========================================================

biodata = get_biodata(username)

if biodata:

    full_name = biodata[2]
    email = biodata[3]
    phone = biodata[4]
    education = biodata[7]
    occupation = biodata[8]
    base_salary = float(biodata[9] or 0)
    financial_goal = biodata[11]

else:

    full_name = username
    email = ""
    phone = ""
    education = ""
    occupation = ""
    base_salary = 0
    financial_goal = ""


# =========================================================
# GET EXPENSES
# =========================================================

expenses = get_expenses(username)

expense_df = pd.DataFrame(
    expenses,
    columns=[
        "Date",
        "Category",
        "Amount",
        "Description"
    ]
)

if not expense_df.empty:

    expense_df["Date"] = pd.to_datetime(
        expense_df["Date"]
    )

    expense_df["Amount"] = pd.to_numeric(
        expense_df["Amount"]
    )

    expense_df["Month"] = (
        expense_df["Date"].dt.to_period("M")
    )


# =========================================================
# GET SAVINGS
# =========================================================

savings = get_savings(username)

saving_df = pd.DataFrame(
    savings,
    columns=[
        "Date",
        "Saving Type",
        "Amount",
        "Description"
    ]
)

if not saving_df.empty:

    saving_df["Date"] = pd.to_datetime(
        saving_df["Date"]
    )

    saving_df["Amount"] = pd.to_numeric(
        saving_df["Amount"]
    )

    saving_df["Month"] = (
        saving_df["Date"].dt.to_period("M")
    )


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title("💰 AI Expense Tracker")

    st.caption(
        "TRACK • SAVE • PREDICT • GROW"
    )

    st.divider()

    st.page_link(
        "pages/Dashboard.py",
        label="📊 Dashboard"
    )

    st.page_link(
        "pages/Add_Expense.py",
        label="💸 Add Expense"
    )

    st.page_link(
        "pages/Add_Saving.py",
        label="🏦 Add Saving"
    )

    st.page_link(
        "pages/Bio_Data.py",
        label="👤 Profile"
    )

    st.divider()

    st.caption(
        f"Logged in as\n**{full_name}**"
    )

    if st.button(
        "🚪 Logout",
        use_container_width=True
    ):

        st.session_state.logged_in = False
        st.session_state.username = ""

        st.switch_page("app.py")


# =========================================================
# HEADER
# =========================================================

st.title("📊 Financial Dashboard")

st.caption(
    "Your complete money journey in one place."
)

st.success(
    f"Welcome back, {full_name}! 👋"
)

st.divider()


# =========================================================
# MONEY FLOW
# =========================================================

st.subheader("💰 Your Money Flow")

flow_cols = st.columns(6)

flow_items = [
    ("💰", "Income"),
    ("💸", "Expenses"),
    ("🏦", "Savings"),
    ("📊", "Analysis"),
    ("🤖", "Prediction"),
    ("🎯", "Goals")
]

for col, (icon, label) in zip(
    flow_cols,
    flow_items
):

    with col:

        st.markdown(
            f"### {icon}"
        )

        st.caption(label)


st.divider()


# =========================================================
# MONTH SELECTOR
# =========================================================

st.subheader("📅 Select Financial Period")

month_names = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"
]

years = set()

if not expense_df.empty:

    years.update(
        expense_df["Date"]
        .dt.year
        .tolist()
    )

if not saving_df.empty:

    years.update(
        saving_df["Date"]
        .dt.year
        .tolist()
    )

years.add(
    pd.Timestamp.today().year
)

years = sorted(years)

year_col, month_col = st.columns(
    [1, 2]
)

with year_col:

    selected_year = st.selectbox(
        "Year",
        years
    )

with month_col:

    selected_month_name = st.selectbox(
        "Month",
        month_names
    )

selected_month_number = (
    month_names.index(
        selected_month_name
    ) + 1
)

selected_period = pd.Period(
    f"{selected_year}-"
    f"{selected_month_number:02d}",
    freq="M"
)


# =========================================================
# MONTHLY SALARY
# =========================================================

st.divider()

st.subheader(
    f"💰 {selected_month_name} "
    f"{selected_year} Income"
)

saved_salary = get_monthly_salary(
    username,
    selected_year,
    selected_month_number
)

if saved_salary is not None:

    salary = float(saved_salary)

else:

    salary = base_salary


salary_col1, salary_col2 = st.columns(
    [2, 1]
)

with salary_col1:

    new_salary = st.number_input(
        "Monthly Income",
        min_value=0.0,
        value=float(salary),
        step=1000.0,
        format="%.2f"
    )

with salary_col2:

    st.write("")
    st.write("")

    if st.button(
        "💾 Save Income",
        use_container_width=True
    ):

        save_monthly_salary(
            username,
            selected_year,
            selected_month_number,
            new_salary
        )

        st.success(
            "Monthly income saved! ✅"
        )

        st.rerun()

if saved_salary is not None:

    st.caption(
        "✅ Using the saved income for this month."
    )

else:

    st.caption(
        "ℹ️ Using the income from your profile."
    )

salary = new_salary


# =========================================================
# SELECTED MONTH EXPENSES
# =========================================================

if not expense_df.empty:

    selected_expenses = expense_df[
        expense_df["Month"] == selected_period
    ]

    monthly_expense = selected_expenses[
        "Amount"
    ].sum()

else:

    selected_expenses = pd.DataFrame()

    monthly_expense = 0


# =========================================================
# SELECTED MONTH SAVINGS
# =========================================================

if not saving_df.empty:

    selected_savings = saving_df[
        saving_df["Month"] == selected_period
    ]

    monthly_savings = selected_savings[
        "Amount"
    ].sum()

else:

    selected_savings = pd.DataFrame()

    monthly_savings = 0


# =========================================================
# BALANCE
# =========================================================

monthly_balance = (
    salary
    - monthly_expense
    - monthly_savings
)


# =========================================================
# FINANCIAL SUMMARY
# =========================================================

st.divider()

st.subheader("💰 Financial Snapshot")

summary_col1, summary_col2, summary_col3, summary_col4 = (
    st.columns(4)
)

with summary_col1:

    st.metric(
        "💰 Income",
        f"₹{salary:,.0f}"
    )

with summary_col2:

    st.metric(
        "💸 Expenses",
        f"₹{monthly_expense:,.0f}"
    )

with summary_col3:

    st.metric(
        "🏦 Savings",
        f"₹{monthly_savings:,.0f}"
    )

with summary_col4:

    st.metric(
        "💵 Balance",
        f"₹{monthly_balance:,.0f}"
    )


# =========================================================
# MONEY ALLOCATION
# =========================================================

st.divider()

with st.container(border=True):
    st.subheader("🔄 Money Allocation")

    allocation_col1, allocation_col2 = st.columns(
        [1, 1]
    )

    expense_percentage = (
        monthly_expense / salary * 100
        if salary > 0
        else 0
    )

    saving_percentage = (
        monthly_savings / salary * 100
        if salary > 0
        else 0
    )

    balance_percentage = (
        monthly_balance / salary * 100
        if salary > 0
        else 0
    )

    with allocation_col1:

        st.write(
            f"💸 **Expenses:** "
            f"{expense_percentage:.1f}%"
        )

        st.progress(
            min(max(expense_percentage / 100, 0), 1)
        )

        st.write(
            f"🏦 **Savings:** "
            f"{saving_percentage:.1f}%"
        )

        st.progress(
            min(max(saving_percentage / 100, 0), 1)
        )

    with allocation_col2:

        st.write(
            f"💵 **Remaining Balance:** "
            f"{balance_percentage:.1f}%"
        )

        st.progress(
            min(max(balance_percentage / 100, 0), 1)
        )

        st.caption(
            "Your allocation is calculated from "
            "income, expenses and savings for the selected month."
        )

# =========================================================
# PERSONAL PROFILE + GOAL
# =========================================================

st.divider()

with st.container(border=True):
    profile_col, goal_col = st.columns(
        [1, 1]
    )

    with profile_col:

        st.subheader("👤 Profile")

        st.write(
            f"**Name:** {full_name}"
        )

        st.write(
            f"**Email:** {email}"
        )

        st.write(
            f"**Phone:** {phone}"
        )

        st.write(
            f"**Education:** {education}"
        )

        st.write(
            f"**Occupation:** {occupation}"
        )


    with goal_col:

        st.subheader("🎯 Financial Goal")

        if financial_goal:

            st.info(
                f"🎯 **Your Goal**\n\n"
                f"{financial_goal}"
            )

        else:

            st.info(
                "Add a financial goal in your "
                "profile to see it here."
            )

# =========================================================
# EXPENSE OVERVIEW
# =========================================================

st.divider()

st.subheader(
    f"💸 {selected_month_name} "
    f"{selected_year} Expenses"
)

st.metric(
    "Total Spending",
    f"₹{monthly_expense:,.0f}"
)

if not selected_expenses.empty:

    display_df = selected_expenses[
        [
            "Date",
            "Category",
            "Amount",
            "Description"
        ]
    ].copy()

    display_df["Date"] = (
        display_df["Date"]
        .dt.strftime("%Y-%m-%d")
    )

    display_df["Amount"] = (
        display_df["Amount"]
        .apply(
            lambda x: f"₹{x:,.0f}"
        )
    )

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        f"No expenses recorded for "
        f"{selected_month_name} "
        f"{selected_year}."
    )


# =========================================================
# SPENDING ANALYSIS
# =========================================================

st.divider()

with st.container(border=True):
    st.subheader("📊 Spending Analysis")

    if not selected_expenses.empty:

        category_df = (
            selected_expenses
            .groupby("Category")["Amount"]
            .sum()
            .reset_index()
            .sort_values(
                "Amount",
                ascending=False
            )
        )

        chart_col1, chart_col2 = st.columns(
            [1, 1]
        )

        # -----------------------------------------------------
        # CATEGORY CHART
        # -----------------------------------------------------

        with chart_col1:

            fig_category = go.Figure()

            fig_category.add_trace(
                go.Bar(
                    x=category_df["Category"],
                    y=category_df["Amount"],
                    text=[
                        f"₹{amount:,.0f}"
                        for amount
                        in category_df["Amount"]
                    ],
                    textposition="outside",
                    marker=dict(
                        color="#29B6F6"
                    ),
                    hovertemplate=(
                        "<b>%{x}</b><br>"
                        "Amount: ₹%{y:,.0f}"
                        "<extra></extra>"
                    )
                )
            )

            fig_category.update_layout(
                title="💸 Spending by Category",
                height=430,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(5,25,50,0.45)",
                font=dict(
                    color="white"
                ),
                xaxis=dict(
                    showgrid=False,
                    tickfont=dict(
                        color="white"
                    )
                ),
                yaxis=dict(
                    gridcolor="rgba(120,180,220,0.15)",
                    tickfont=dict(
                        color="white"
                    )
                ),
                margin=dict(
                    l=40,
                    r=20,
                    t=70,
                    b=80
                )
            )

            st.plotly_chart(
                fig_category,
                use_container_width=True
            )


        # -----------------------------------------------------
        # DONUT CHART
        # -----------------------------------------------------

        with chart_col2:

            fig_donut = go.Figure()

            fig_donut.add_trace(
                go.Pie(
                    labels=category_df["Category"],
                    values=category_df["Amount"],
                    hole=0.55,
                    textinfo="label+percent",
                    hovertemplate=(
                        "<b>%{label}</b><br>"
                        "₹%{value:,.0f}"
                        "<extra></extra>"
                    )
                )
            )

            fig_donut.update_layout(
                title="📊 Expense Distribution",
                height=430,
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(
                    color="white"
                ),
                legend=dict(
                    font=dict(
                        color="white"
                    )
                ),
                margin=dict(
                    l=20,
                    r=20,
                    t=70,
                    b=20
                )
            )

            st.plotly_chart(
                fig_donut,
                use_container_width=True
            )

    else:

        st.info(
            "💸 Add expenses to see your spending analysis."
        )

# =========================================================
# AI EXPENSE PREDICTION
# =========================================================

st.divider()

with st.container(border=True):
    st.subheader("🤖 AI Expense Prediction")

    st.caption(
        "Linear Regression learns from your recorded "
        "monthly expenses and estimates the next month."
    )

    if not expense_df.empty:

        prediction_data = expense_df[
            expense_df["Month"] <= selected_period
        ]

        monthly_data = (
            prediction_data
            .groupby("Month")["Amount"]
            .sum()
            .reset_index()
            .sort_values("Month")
        )

        if len(monthly_data) >= 2:

            X = [
                [i]
                for i in range(
                    len(monthly_data)
                )
            ]

            y = monthly_data[
                "Amount"
            ].tolist()

            model = LinearRegression()

            model.fit(
                X,
                y
            )

            next_number = len(
                monthly_data
            )

            prediction = model.predict(
                [[next_number]]
            )[0]

            prediction = max(
                0,
                prediction
            )

            next_month = (
                selected_period + 1
            )

            next_month_name = (
                next_month.strftime(
                    "%B %Y"
                )
            )

            prediction_col1, prediction_col2 = (
                st.columns(2)
            )

            with prediction_col1:

                st.metric(
                    "🤖 Predicted Expense",
                    f"₹{prediction:,.0f}"
                )

            with prediction_col2:

                st.metric(
                    "📅 Prediction Month",
                    next_month_name
                )

            # Prediction trend chart

            chart_months = [
                period.strftime("%b %Y")
                for period
                in monthly_data["Month"]
            ]

            actual_values = (
                monthly_data["Amount"]
                .tolist()
            )

            prediction_months = (
                chart_months
                + [next_month_name]
            )

            prediction_values = (
                actual_values
                + [prediction]
            )

            fig_prediction = go.Figure()

            fig_prediction.add_trace(
                go.Scatter(
                    x=chart_months,
                    y=actual_values,
                    mode="lines+markers",
                    name="Recorded",
                    line=dict(
                        color="#29B6F6",
                        width=4
                    ),
                    marker=dict(
                        size=10
                    )
                )
            )

            fig_prediction.add_trace(
                go.Scatter(
                    x=prediction_months[-2:],
                    y=prediction_values[-2:],
                    mode="lines+markers",
                    name="Prediction",
                    line=dict(
                        color="#914DFF",
                        width=4,
                        dash="dash"
                    ),
                    marker=dict(
                        size=11
                    )
                )
            )

            fig_prediction.update_layout(
                title="📈 Expense Trend & Prediction",
                height=430,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(5,25,50,0.45)",
                font=dict(
                    color="white"
                ),
                xaxis=dict(
                    showgrid=False,
                    tickfont=dict(
                        color="white"
                    )
                ),
                yaxis=dict(
                    title="Amount (₹)",
                    gridcolor="rgba(120,180,220,0.15)",
                    tickfont=dict(
                        color="white"
                    )
                ),
                legend=dict(
                    font=dict(
                        color="white"
                    )
                )
            )

            st.plotly_chart(
                fig_prediction,
                use_container_width=True
            )

            st.caption(
                "Prediction is based only on the "
                "monthly expense data recorded in the app."
            )

        else:

            st.info(
                "🌱 Add expenses in at least 2 different "
                "months to generate an AI prediction."
            )

    else:

        st.info(
            "💸 Add expenses to generate an AI prediction."
        )

# =========================================================
# SMART INSIGHTS
# =========================================================

st.divider()

suggestions = []

if monthly_expense > salary and salary > 0:

    suggestions.append(
        "⚠️ Your expenses are higher than "
        "your monthly income."
    )

elif salary > 0 and monthly_expense > salary * 0.50:

    suggestions.append(
        "💡 More than 50% of your income "
        "has been spent."
    )

elif salary > 0:

    suggestions.append(
        "✅ Your current expenses are within "
        "50% of your income."
    )

if monthly_savings > 0:

    suggestions.append(
        f"🏦 You saved ₹{monthly_savings:,.0f} "
        "this month."
    )

else:

    suggestions.append(
        "🌱 Try setting aside a small amount "
        "for savings this month."
    )

if not selected_expenses.empty:

    category_totals = (
        selected_expenses
        .groupby("Category")["Amount"]
        .sum()
    )

    highest_category = (
        category_totals.idxmax()
    )

    highest_amount = (
        category_totals.max()
    )

    suggestions.append(
        f"📌 Highest spending category: "
        f"{highest_category} "
        f"(₹{highest_amount:,.0f})."
    )

insight_html = """
<div class="white-card">
    <h2>💡 Smart Financial Insights</h2>
"""

for suggestion in suggestions:
    insight_html += f"<p>{suggestion}</p>"

insight_html += "</div>"

st.markdown(
    insight_html,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="white-card">
        <h2>🌱 Saving Tip</h2>
        <div class="tip-title">Small savings, big dreams!</div>
        <p>
            Saving a small amount regularly can help you
            build toward your financial goals.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# =========================================================
# GOAL SUMMARY
# =========================================================

st.divider()

if financial_goal:

    goal_content = f"""
    <div class="white-card">
        <h2>🎯 Keep Moving Toward Your Goal</h2>
        <p class="goal-text">🎯 Current Goal: {financial_goal}</p>
    </div>
    """

else:

    goal_content = """
    <div class="white-card">
        <h2>🎯 Keep Moving Toward Your Goal</h2>
        <p class="goal-text">
            Add a financial goal in your profile to display it here.
        </p>
    </div>
    """

st.markdown(
    goal_content,
    unsafe_allow_html=True
)

# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "💰 Track your income  •  "
    "💸 Understand your spending  •  "
    "🏦 Build your savings  •  "
    "🤖 Predict your future  •  "
    "🎯 Reach your goals"
)