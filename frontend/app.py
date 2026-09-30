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

# -----------------------------
# Dashboard
# -----------------------------

st.header("📊 Expense Dashboard")

try:
    expenses_response = requests.get(f"{API_URL}/expenses")
    total_response = requests.get(f"{API_URL}/expenses/total")

    if expenses_response.status_code == 200:
        expenses = expenses_response.json()

        if expenses:
            df = pd.DataFrame(expenses)

            col1, col2, col3 = st.columns(3)

            col1.metric("Total Expenses", f"₹{df['amount'].sum():,.2f}")
            col2.metric("Number of Expenses", len(df))
            col3.metric("Average Expense", f"₹{df['amount'].mean():,.2f}")

            st.subheader("📋 Expense Records")
            st.dataframe(df, use_container_width=True)

            st.subheader("📈 Spending by Category")

            category_data = df.groupby("category")["amount"].sum()

            st.bar_chart(category_data)

        else:
            st.info("No expenses found.")

    else:
        st.error("Could not connect to FastAPI.")

except Exception as e:
    st.error(f"Connection error: {e}")


# -----------------------------
# AI Chat
# -----------------------------

st.header("🤖 Smart Expense AI Agent")

question = st.text_input(
    "Ask something about your expenses:",
    placeholder="Example: How much did I spend this month?"
)

if st.button("Ask AI"):

    if question.strip():

        try:
            response = requests.post(
                f"{API_URL}/ai-agent",
                params={"query": question}
            )

            if response.status_code == 200:

                result = response.json()

                st.success("AI Response")

                st.write(result["response"])

            else:
                st.error(
                    f"AI Agent Error: {response.status_code}"
                )

        except Exception as e:
            st.error(f"Connection error: {e}")

    else:
        st.warning("Please enter a question.")
