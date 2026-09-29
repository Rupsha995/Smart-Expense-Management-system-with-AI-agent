from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from pydantic import BaseModel, Field
from datetime import date
from backend.ml_model import predict_next_month
from backend.ai_agent import ask_ai
from backend.database import engine, get_db, Base
from backend.models import Expense

app = FastAPI(title="Smart Expense Management API")

Base.metadata.create_all(bind=engine)


class ExpenseCreate(BaseModel):
    title: str
    category: str
    amount: float = Field(gt=0)
    expense_date: date


@app.get("/")
def home():
    return {"message": "Smart Expense API is running"}


@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"status": "healthy", "database": "connected"}


@app.post("/expenses")
def add_expense(
    expense: ExpenseCreate,
    db: Session = Depends(get_db)
):
    new_expense = Expense(
        title=expense.title,
        category=expense.category,
        amount=expense.amount,
        expense_date=expense.expense_date
    )

    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)

    return {
        "message": "Expense added successfully",
        "expense_id": new_expense.id
    }


@app.get("/expenses")
def get_expenses(db: Session = Depends(get_db)):
    expenses = db.query(Expense).all()

    return [
        {
            "id": e.id,
            "title": e.title,
            "category": e.category,
            "amount": e.amount,
            "expense_date": e.expense_date
        }
        for e in expenses
    ]


@app.get("/expenses/total")
def total_expenses(db: Session = Depends(get_db)):
    total = db.query(
        text("COALESCE(SUM(amount), 0)")
    ).select_from(Expense).scalar()

    return {"total_expenses": float(total)}
@app.get("/expenses/summary")
def expense_summary(db: Session = Depends(get_db)):

    # Total expense
    total = db.query(
        text("COALESCE(SUM(amount), 0)")
    ).select_from(Expense).scalar()

    # Average expense
    average = db.query(
        text("COALESCE(AVG(amount), 0)")
    ).select_from(Expense).scalar()

    # Category-wise expense
    category_data = db.query(
        Expense.category,
        text("SUM(amount)")
    ).group_by(Expense.category).all()

    category_breakdown = {
        category: float(amount)
        for category, amount in category_data
    }

    # Highest spending category
    highest_category = None

    if category_breakdown:
        highest_category = max(
            category_breakdown,
            key=category_breakdown.get
        )

    return {
        "total_expense": float(total),
        "average_expense": round(float(average), 2),
        "highest_category": highest_category,
        "category_breakdown": category_breakdown
    }

@app.post("/ai-agent")
def ai_agent_query(
    query: str,
    db: Session = Depends(get_db)
):
    result = ask_ai(query, db)

    return result