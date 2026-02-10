import pandas as pd

def normalize_expenses(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["amount_spent"] = (
        df["amount_spent"]
        .replace({"£": "", ",": ""}, regex=True)
        .astype(float)
    )
    df["expense_date"] = pd.to_datetime(df["expense_date"], errors="coerce").dt.date
    df["billing_date"] = pd.to_datetime(df["billing_date"], errors="coerce").dt.date

    df = df.sort_values("expense_date").reset_index(drop=True)
    return df