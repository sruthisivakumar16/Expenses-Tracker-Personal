import pandas as pd


def monthly_totals(df: pd.DataFrame) -> pd.Series:
    return df.groupby("month")["amount_spent"].sum().sort_values(ascending=False)


def category_totals(df: pd.DataFrame) -> pd.Series:
    return df.groupby("expense_category")["amount_spent"].sum().sort_values(ascending=False)


def merchant_totals(df: pd.DataFrame, top_n: int = 10) -> pd.Series:
    return (df.groupby("name")["amount_spent"].sum()
              .sort_values(ascending=False)
              .head(top_n))


def daily_totals(df):
    daily = df.groupby("expense_date")["amount_spent"].sum().sort_index()
    daily.index = pd.to_datetime(daily.index)  # ensure datetime index
    return daily


def rolling_7d_spend(df: pd.DataFrame) -> pd.Series:
    return daily_totals(df).rolling("7D").sum()


def daily_with_rolling_avg(df: pd.DataFrame, window: str = "7D") -> pd.DataFrame:
    daily = daily_totals(df)
    full_range = pd.date_range(daily.index.min(), daily.index.max(), freq="D")
    daily = daily.reindex(full_range, fill_value=0)
    rolling_avg = daily.rolling(window).mean()
    return pd.DataFrame({"daily": daily, "rolling_avg": rolling_avg})
