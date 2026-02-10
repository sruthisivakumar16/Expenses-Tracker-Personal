import os

import pandas as pd
import streamlit as st

from src.config import GOOGLE_SHEET_ID, SCOPE, SERVICE_ACCOUNT_JSON_PATH
from src.processing.clean import normalize_expenses
from src.processing.metrics import (
    category_totals,
    daily_with_rolling_avg,
    merchant_totals,
    monthly_totals,
)
from src.services.load_sheets_data import DEFAULT_EXCLUDED_TABS, load_sheets_data
from src.services.sheets_auth import get_gspread_client
from src.visualisations.charts import (
    bar_by_month,
    bar_recurring_expenses,
    bar_top_merchants,
    line_daily_with_rolling,
    pie_by_category,
)

st.set_page_config(page_title="Expenses Dashboard", layout="wide")
st.title("Expenses Dashboard")

st.sidebar.header("Configuration")

sheet_id = st.sidebar.text_input("Google Sheet ID", GOOGLE_SHEET_ID)
service_account_path = st.sidebar.text_input(
    "Service Account JSON Path", SERVICE_ACCOUNT_JSON_PATH
)

scopes = [scope.strip() for scope in SCOPE.split(",") if scope.strip()]


@st.cache_data(ttl=600)
def load_data(sheet_id: str, service_account_path: str, scopes: list[str]) -> pd.DataFrame:
    if not sheet_id:
        return pd.DataFrame()

    if not os.path.exists(service_account_path):
        st.error("Service account file not found.")
        return pd.DataFrame()

    gc = get_gspread_client(service_account_path, scopes)
    data = load_sheets_data(sheet_id, gc, excluded_tabs=DEFAULT_EXCLUDED_TABS)
    if data.empty:
        return pd.DataFrame()

    data = data.rename(columns={"worksheet": "month"})
    return normalize_expenses(data)


combined = load_data(sheet_id, service_account_path, scopes)

if combined.empty:
    st.info("Enter a valid Sheet ID and service account JSON path to load data.")
    st.stop()

exclude_tabs = {"form responses", "form responses 1", "responses"}
months = [
    month
    for month in sorted(combined["month"].dropna().unique())
    if month.strip().lower() not in exclude_tabs
]
months = ["All"] + months
selected_month = st.sidebar.selectbox("Month", months)
filtered = combined if selected_month == "All" else combined[combined["month"] == selected_month]

exclude_fixed = st.sidebar.toggle("Exclude rent & utilities", value=False)
if exclude_fixed:
    excluded_categories = {"rent", "utilities"}
    filtered = filtered[~filtered["expense_category"].str.lower().isin(excluded_categories)]

st.subheader("Overview")
top_row = st.columns(5)
today = pd.Timestamp.today().date()
seven_days_ago = today - pd.Timedelta(days=6)
spent_today = filtered[filtered["expense_date"] == today]["amount_spent"].sum()
spent_7d = filtered[filtered["expense_date"] >= seven_days_ago]["amount_spent"].sum()
top_row[0].metric("Total Spend", f"£{filtered['amount_spent'].sum():,.2f}")
top_row[1].metric("Spent Today", f"£{spent_today:,.2f}")
top_row[2].metric("Last 7 Days", f"£{spent_7d:,.2f}")
top_row[3].metric("Transactions", f"{len(filtered):,}")
top_row[4].metric(
    "Avg Spend",
    f"£{filtered['amount_spent'].mean():,.2f}" if not filtered.empty else "£0.00",
)

st.subheader("Highlights")
left, right = st.columns(2)

monthly_source = filtered if selected_month != "All" else combined
monthly = monthly_totals(monthly_source)
left.plotly_chart(
    bar_by_month(monthly),
    use_container_width=True,
    config={"displayModeBar": True, "displaylogo": False},
)

category = category_totals(filtered)
right.plotly_chart(
    pie_by_category(category),
    use_container_width=True,
    config={"displayModeBar": True, "displaylogo": False},
)

st.subheader("Trends")
trend_left, trend_right = st.columns(2)

daily_with_avg = daily_with_rolling_avg(filtered)
trend_left.plotly_chart(
    line_daily_with_rolling(daily_with_avg),
    use_container_width=True,
    config={"displayModeBar": True, "displaylogo": False},
)

merchants = merchant_totals(filtered)
trend_right.plotly_chart(
    bar_top_merchants(merchants),
    use_container_width=True,
    config={"displayModeBar": True, "displaylogo": False},
)

st.subheader("Recurring Expenses")
recurring_only = filtered[filtered["recurring"].str.lower() == "yes"]
recurring_col, recurring_total_col = st.columns(2)
recurring_col.plotly_chart(
    bar_recurring_expenses(recurring_only),
    use_container_width=True,
    config={"displayModeBar": True, "displaylogo": False},
)
recurring_total = recurring_only["amount_spent"].sum()
recurring_total_col.metric("Total Recurring", f"£{recurring_total:,.2f}")

with st.expander("Raw Data"):
    st.dataframe(filtered)
