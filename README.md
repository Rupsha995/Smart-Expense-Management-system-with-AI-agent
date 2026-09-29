# Smart-Expense-Management-system-with-AI-agent
# 💰 Smart Expense Management System with AI Agent

An AI-powered Smart Expense Management System that helps users track, analyze, and understand their spending. The application combines **FastAPI, MySQL, Machine Learning, Streamlit, and Groq LLM** to provide expense analytics and an interactive AI assistant.

## 🚀 Features

* Add and manage expense records
* Store expense data in MySQL
* Calculate total and average expenses
* Analyze spending by category
* Visualize expenses using charts
* Predict future expenses using Machine Learning
* Ask questions about expenses using an AI Agent
* Generate simple budgeting suggestions
* REST API using FastAPI
* Interactive Streamlit dashboard

## 🏗️ Architecture

```text
                  ┌──────────────────────┐
                  │      Streamlit       │
                  │     Dashboard UI     │
                  └──────────┬───────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │       FastAPI        │
                  │      REST APIs       │
                  └──────────┬───────────┘
                             │
                ┌────────────┴────────────┐
                ▼                         ▼
       ┌─────────────────┐       ┌─────────────────┐
       │      MySQL      │       │    Groq LLM     │
       │ Expense Database│       │    AI Agent      │
       └─────────────────┘       └─────────────────┘
```

## 🛠️ Technologies Used

| Technology   | Purpose              |
| ------------ | -------------------- |
| Python       | Backend development  |
| FastAPI      | REST API             |
| MySQL        | Expense database     |
| SQLAlchemy   | Database ORM         |
| Streamlit    | Web dashboard        |
| Pandas       | Data analysis        |
| NumPy        | Numerical operations |
| Scikit-learn | Machine Learning     |
| Groq         | LLM integration      |
| Requests     | API communication    |
| Uvicorn      | FastAPI server       |

## 📂 Project Structure

```text
smart_expense_agent/
│
├── backend/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── ml_model.py
│   └── ai_agent.py
│
├── frontend/
│   └── app.py
│
├── .env
├── requirements.txt
└── README.md
```

## 🤖 AI Agent

The AI Agent connects the user's question with expense information stored in MySQL.

For example:

```text
User:
How much did I spend this month?

AI Agent:
You spent ₹9,850 this month.
Food: ₹6,350
```
