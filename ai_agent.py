import os
from datetime import date

from dotenv import load_dotenv
from groq import Groq
from sqlalchemy.orm import Session
from sqlalchemy import extract

from backend.models import Expense

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def ask_ai(question: str, db: Session):

    # Get current month and year
    today = date.today()

    # Fetch expenses from MySQL
    expenses = db.query(Expense).filter(
        extract("month", Expense.expense_date) == today.month,
        extract("year", Expense.expense_date) == today.year
    ).all()

    # Calculate total
    total_expense = sum(e.amount for e in expenses)

    # Category breakdown
    category_breakdown = {}

    for e in expenses:
        category_breakdown[e.category] = (
            category_breakdown.get(e.category, 0) + e.amount
        )

    # Data sent to Groq
    expense_data = {
        "month": today.strftime("%B %Y"),
        "total_expense": total_expense,
        "category_breakdown": category_breakdown
    }

    prompt = f"""
You are a Smart Expense AI Agent.

The following is the user's REAL expense data retrieved from MySQL:

{expense_data}

User question:
{question}

Instructions:
- Answer using the expense data above.
- Do not invent amounts.
- Do not say you cannot access the expense records.
- Keep the answer simple and clear.
- If appropriate, give a short budgeting suggestion.
"""

    # Send MySQL data + question to Groq
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful Smart Expense Management AI Agent."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return {
        "query": question,
        "response": response.choices[0].message.content,
        "expense_data": expense_data
    }