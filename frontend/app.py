```python
import streamlit as st
import requests
import pandas as pd

API_URL = "https://smart-expense-management-system-with-ai-wqi3.onrender.com"

st.set_page_config(
    page_title="Smart Expense Manager",
    page_icon="💰",
    layout="wide"
)

st.title("💰 Smart Expense Management System")
st.write("Track your expenses and ask questions using the AI Agent.")

# ============================================================
# ADD EXPENSE
# ============================================================

st.header("➕ Add New Expense")

with st.form("expense_form"):
    title = st.text_input(
        "Expense Title",
        placeholder="Example: Lunch"
    )

    category = st.selectbox(
        "Category",
        [
            "Food",
            "Transport",
            "Shopping",
            "Entertainment",
            "Bills",
            "Education",
            "Health",
            "Travel",
            "Other"
        ]
    )

    amount = st.number_input(
        "Amount (₹)",
        min_value=0.0,
        step=1.0
    )

    expense_date = st.date_input(
        "Expense Date"
    )

    submitted = st.form_submit_button("➕ Add Expense")

    if submitted:

        if not title.strip():
            st.warning("Please enter an expense title.")

        elif amount <= 0:
            st.warning("Please enter an amount greater than 0.")

        else:
            try:
                response = requests.post(
                    f"{API_URL}/expenses",
                    json={
                        "title": title,
                        "category": category,
                        "amount": amount,
                        "expense_date": expense_date.isoformat()
                    }
                )

                if response.status_code in [200, 201]:
                    st.success("✅ Expense added successfully!")
                    st.rerun()

                else:
                    st.error(
                        f"Failed to add expense. "
                        f"Status: {response.status_code}"
                    )
                    st.code(response.text)

            except Exception as e:
                st.error(f"Connection error: {e}")


# ============================================================
# EXPENSE DASHBOARD
# ============================================================

st.header("📊 Expense Dashboard")

try:

    expenses_response = requests.get(
        f"{API_URL}/expenses"
    )

    if expenses_response.status_code == 200:

        expenses = expenses_response.json()

        if expenses:

            df = pd.DataFrame(expenses)

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Total Expenses",
                f"₹{df['amount'].sum():,.2f}"
            )

            col2.metric(
                "Number of Expenses",
                len(df)
            )

            col3.metric(
                "Average Expense",
                f"₹{df['amount'].mean():,.2f}"
            )

            st.subheader("📋 Expense Records")

            st.dataframe(
                df,
                use_container_width=True
            )

            st.subheader("📈 Spending by Category")

            category_data = (
                df.groupby("category")["amount"]
                .sum()
            )

            st.bar_chart(category_data)

        else:

            st.info(
                "No expenses found. "
                "Add your first expense above."
            )

    else:

        st.error(
            f"Could not get expenses. "
            f"Status: {expenses_response.status_code}"
        )

except Exception as e:

    st.error(
        f"Connection error: {e}"
    )


# ============================================================
# AI AGENT
# ============================================================

st.header("🤖 Smart Expense AI Agent")

question = st.text_input(
    "Ask something about your expenses:",
    placeholder="Example: How much did I spend this month?"
)

if st.button("🤖 Ask AI"):

    if question.strip():

        try:

            response = requests.post(
                f"{API_URL}/ai-agent",
                params={
                    "query": question
                }
            )

            if response.status_code == 200:

                result = response.json()

                st.success("AI Response")

                st.write(
                    result["response"]
                )

            else:

                st.error(
                    f"AI Agent Error: "
                    f"{response.status_code}"
                )

                st.code(response.text)

        except Exception as e:

            st.error(
                f"Connection error: {e}"
            )

    else:

        st.warning(
            "Please enter a question."
        )
```
