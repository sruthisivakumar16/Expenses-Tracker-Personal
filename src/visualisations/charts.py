import plotly.express as px
import pandas as pd


def pie_by_category(category_totals: pd.Series):
    df = category_totals.reset_index()
    df.columns = ["category", "amount"]
    fig = px.pie(
        df,
        names="category",
        values="amount",
        hole=0.4,
        title="Spend by Category",
    )
    fig.update_traces(textposition="inside", textinfo="percent+label")
    return fig


def bar_by_month(monthly_totals: pd.Series):
    df = monthly_totals.reset_index()
    df.columns = ["month", "amount"]
    fig = px.bar(
        df,
        x="month",
        y="amount",
        title="Monthly Spend",
        text_auto=True,
        color="amount",
        color_continuous_scale="Blues",
    )
    return fig


def line_rolling_spend(rolling_series: pd.Series):
    df = rolling_series.reset_index()
    df.columns = ["date", "amount"]
    fig = px.line(
        df,
        x="date",
        y="amount",
        title="7‑Day Rolling Spend",
        markers=True,
    )
    return fig


def line_daily_with_rolling(daily_with_avg: pd.DataFrame):
    df = daily_with_avg.reset_index().rename(columns={"index": "date"})
    fig = px.line(
        df,
        x="date",
        y=["daily", "rolling_avg"],
        title="Daily Spend with 7‑Day Average",
        markers=True,
    )
    fig.update_layout(legend_title_text="")
    return fig


def bar_top_merchants(merchant_totals: pd.Series):
    df = merchant_totals.reset_index()
    df.columns = ["merchant", "amount"]
    fig = px.bar(
        df,
        x="amount",
        y="merchant",
        orientation="h",
        title="Top Merchants",
        text_auto=True,
        color="amount",
        color_continuous_scale="Teal",
    )
    fig.update_layout(yaxis=dict(autorange="reversed"))
    return fig


def bar_recurring_expenses(recurring_df: pd.DataFrame):
    df = recurring_df.sort_values("amount_spent", ascending=False)
    fig = px.bar(
        df,
        x="amount_spent",
        y="name",
        color="fixed",
        orientation="h",
        title="Recurring Expenses",
        text_auto=True,
        color_discrete_map={"Yes": "#636EFA", "No": "#EF553B"},
    )
    fig.update_layout(yaxis=dict(autorange="reversed"), legend_title_text="Fixed")
    return fig
