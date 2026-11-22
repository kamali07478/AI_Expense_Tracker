import streamlit as st
import os
import base64
import streamlit.components.v1 as components
from datetime import date

from database import add_saving
from theme import set_background, require_login


# -----------------------------
# PAGE CONFIGURATION
# -----------------------------

st.set_page_config(
    page_title="Add Saving",
    page_icon="🏦",
    layout="wide"
)


# -----------------------------
# BACKGROUND
# -----------------------------

set_background("images/add_saving_background.png")


# -----------------------------
# LOGIN CHECK
# -----------------------------

require_login()

username = st.session_state.get("username", "")


# -----------------------------
# HEADER
# -----------------------------

st.title("🏦 Add Saving")
st.caption("SAVE TODAY • BUILD YOUR FUTURE")
st.divider()


# -----------------------------
# MONEY FLOW
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
# SAVING FORM
# -----------------------------

st.subheader("📝 Saving Details")

st.caption(
    "Record your savings and build better financial habits."
)

col1, col2 = st.columns(2, gap="large")


with col1:

    saving_date = st.date_input(
        "📅 Saving Date",
        value=date.today()
    )

    saving_type = st.selectbox(
        "🏷️ Saving Type",
        [
            "General Saving",
            "Gold",
            "Stock Market",
            "Bank Deposit",
            "Emergency Fund",
            "Other"
        ]
    )


with col2:

    amount = st.number_input(
        "💰 Saving Amount",
        min_value=0.0,
        step=100.0,
        format="%.2f"
    )

    description = st.text_area(
        "📝 Description",
        placeholder="Example: Monthly saving, emergency fund...",
        height=120
    )


st.divider()


# -----------------------------
# SAVING PREVIEW
# -----------------------------

st.subheader("👀 Saving Preview")

preview_col1, preview_col2, preview_col3 = st.columns(3)


with preview_col1:

    st.metric(
        "Saving Type",
        saving_type
    )


with preview_col2:

    st.metric(
        "Amount",
        f"₹{amount:,.2f}"
    )


with preview_col3:

    st.metric(
        "Date",
        saving_date.strftime("%d %b %Y")
    )


st.divider()


# -----------------------------
# ADD SAVING BUTTON
# -----------------------------

if st.button(
    "🏦 Add Saving",
    use_container_width=True
):

    # -----------------------------
    # VALIDATE AMOUNT
    # -----------------------------

    if amount <= 0:

        st.warning(
            "⚠️ Please enter a valid saving amount."
        )

    else:

        # -----------------------------
        # ADD SAVING TO DATABASE
        # -----------------------------

        add_saving(
            username,
            saving_date,
            saving_type,
            amount,
            description
        )


        # -----------------------------
        # SUCCESS MESSAGE
        # -----------------------------

        st.success(
            "🎉 Saving added successfully!"
        )


        # -----------------------------
        # BALLOONS
        # -----------------------------

        st.balloons()


        # -----------------------------
        # FIND GIF
        # -----------------------------

        gif_path = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                "..",
                "saving_celebration_animation.gif"
            )
        )


        # -----------------------------
        # SHOW GIF
        # -----------------------------

        if os.path.isfile(gif_path):

            try:

                # Read GIF file
                with open(gif_path, "rb") as gif_file:

                    gif_data = base64.b64encode(
                        gif_file.read()
                    ).decode("utf-8")


                # Display animated GIF
                components.html(
                    f"""
                    <html>

                    <body style="
                        margin: 0;
                        padding: 0;
                        background: transparent;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                    ">

                        <img
                            src="data:image/gif;base64,{gif_data}"
                            style="
                                width: 450px;
                                max-width: 90%;
                                height: auto;
                                display: block;
                                margin: auto;
                            "
                        >

                    </body>

                    </html>
                    """,

                    height=450,

                    scrolling=False
                )


            except Exception as e:

                st.error(
                    f"❌ Unable to display GIF: {e}"
                )


        else:

            st.error(
                "❌ Celebration GIF not found."
            )