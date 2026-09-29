import pandas as pd
from sklearn.linear_model import LinearRegression


def predict_next_month(expenses):

    if len(expenses) < 2:
        return None

    data = pd.DataFrame(expenses)

    data["expense_date"] = pd.to_datetime(data["expense_date"])

    monthly = (
        data
        .groupby(data["expense_date"].dt.to_period("M"))["amount"]
        .sum()
        .reset_index()
    )

    if len(monthly) < 2:
        return None

    monthly["month_number"] = range(1, len(monthly) + 1)

    X = monthly[["month_number"]]
    y = monthly["amount"]

    model = LinearRegression()
    model.fit(X, y)

    next_month = len(monthly) + 1

    prediction = model.predict([[next_month]])

    return round(float(prediction[0]), 2)