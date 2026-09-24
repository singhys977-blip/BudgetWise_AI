import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import joblib

# Load trained ML model
model = joblib.load("budgetwise_model.pkl")

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="BudgetWise",
    page_icon="💰",
    layout="wide"
)

# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("💰 BudgetWise")
st.subheader("ML-Based Personal Budget Analysis")

st.write(
    "Enter your monthly income and expenses to understand "
    "your spending pattern and savings."
)

st.divider()

# --------------------------------------------------
# USER INPUT
# --------------------------------------------------

st.header("💵 Monthly Financial Information")

income = st.number_input(
    "Monthly Income (₹)",
    min_value=0.0,
    value=50000.0,
    step=1000.0
)

col1, col2, col3 = st.columns(3)

with col1:
    rent = st.number_input(
        "🏠 Rent",
        min_value=0.0,
        value=10000.0,
        step=500.0
    )

    food = st.number_input(
        "🍔 Food",
        min_value=0.0,
        value=5000.0,
        step=500.0
    )

    transport = st.number_input(
        "🚗 Transport",
        min_value=0.0,
        value=3000.0,
        step=500.0
    )

with col2:
    shopping = st.number_input(
        "🛍️ Shopping",
        min_value=0.0,
        value=3000.0,
        step=500.0
    )

    entertainment = st.number_input(
        "🎬 Entertainment",
        min_value=0.0,
        value=2000.0,
        step=500.0
    )

    healthcare = st.number_input(
        "🏥 Healthcare",
        min_value=0.0,
        value=1000.0,
        step=500.0
    )

with col3:
    education = st.number_input(
        "🎓 Education",
        min_value=0.0,
        value=1000.0,
        step=500.0
    )

    bills = st.number_input(
        "💡 Bills",
        min_value=0.0,
        value=2000.0,
        step=500.0
    )

    other = st.number_input(
        "📦 Other",
        min_value=0.0,
        value=1000.0,
        step=500.0
    )

# --------------------------------------------------
# CALCULATIONS
# --------------------------------------------------

total_expenses = (
    rent
    + food
    + transport
    + shopping
    + entertainment
    + healthcare
    + education
    + bills
    + other
)

savings = income - total_expenses

if income > 0:
    savings_percentage = (savings / income) * 100
else:
    savings_percentage = 0

# --------------------------------------------------
# BUTTON
# --------------------------------------------------

if st.button("🔍 Analyze My Budget", type="primary"):
        # Prepare input for ML model
    input_data = pd.DataFrame([{
        "Income": income,
        "Rent": rent,
        "Food": food,
        "Transport": transport,
        "Shopping": shopping,
        "Entertainment": entertainment,
        "Healthcare": healthcare,
        "Education": education,
        "Bills": bills,
        "Other": other
    }])

    # ML prediction
    predicted_expenses = model.predict(input_data)[0]

    st.divider()

    st.header("📊 Your Budget Analysis")
    st.subheader("🤖 Machine Learning Prediction")

    st.info(
        f"Predicted Monthly Expenses: ₹{predicted_expenses:,.2f}"
    )


    # --------------------------------------------------
    # SUMMARY
    # --------------------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Monthly Income",
            f"₹{income:,.0f}"
        )

    with col2:
        st.metric(
            "Total Expenses",
            f"₹{total_expenses:,.0f}"
        )

    with col3:
        st.metric(
            "Savings",
            f"₹{savings:,.0f}"
        )

    # --------------------------------------------------
    # SAVINGS STATUS
    # --------------------------------------------------

    st.subheader("💰 Savings Status")

    if savings > 0:
        st.success(
            f"You have ₹{savings:,.0f} left after your expenses."
        )
    elif savings == 0:
        st.warning(
            "Your income and expenses are equal. "
            "There is no amount left for savings."
        )
    else:
        st.error(
            f"Your expenses are ₹{abs(savings):,.0f} higher "
            "than your income."
        )

    st.write(
        f"**Savings Percentage:** {savings_percentage:.1f}%"
    )

    # --------------------------------------------------
    # EXPENSE DATA
    # --------------------------------------------------

    expense_data = pd.DataFrame({
        "Category": [
            "Rent",
            "Food",
            "Transport",
            "Shopping",
            "Entertainment",
            "Healthcare",
            "Education",
            "Bills",
            "Other"
        ],
        "Amount": [
            rent,
            food,
            transport,
            shopping,
            entertainment,
            healthcare,
            education,
            bills,
            other
        ]
    })

    expense_data = expense_data[
        expense_data["Amount"] > 0
    ]

    # --------------------------------------------------
    # EXPENSE CHART
    # --------------------------------------------------

    st.subheader("📈 Expense Breakdown")

    fig, ax = plt.subplots()

    ax.bar(
        expense_data["Category"],
        expense_data["Amount"]
    )

    ax.set_xlabel("Expense Category")
    ax.set_ylabel("Amount (₹)")
    ax.set_title("Monthly Expense Breakdown")

    plt.xticks(rotation=45)

    st.pyplot(fig)

    # --------------------------------------------------
    # HIGHEST EXPENSE
    # --------------------------------------------------

    highest_category = expense_data.loc[
        expense_data["Amount"].idxmax(),
        "Category"
    ]

    highest_amount = expense_data["Amount"].max()

    st.info(
        f"Your highest expense category is **{highest_category}** "
        f"at ₹{highest_amount:,.0f}."
    )

    # --------------------------------------------------
    # BASIC BUDGET STATUS
    # --------------------------------------------------

    st.subheader("📌 Budget Status")

    if savings_percentage >= 20:
        st.success(
            "Your current savings are at or above 20% of income."
        )

    elif savings_percentage > 0:
        st.warning(
            "You are saving money, but your savings percentage "
            "is below 20%."
        )

    else:
        st.error(
            "Your current expenses are equal to or higher than "
            "your income."
        )