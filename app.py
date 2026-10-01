"""Streamlit dashboard: streamlit run app.py"""
import pandas as pd
import plotly.express as px
import streamlit as st

from scm.analytics import (abc_classification, exponential_smoothing_forecast,
                           mape, moving_average_forecast, sku_policy_table)

st.set_page_config(page_title="Supply Chain Analyst", layout="wide")
st.title("Supply Chain Analytics & Inventory Optimization")

file = st.sidebar.file_uploader("Sales CSV (date, sku, units, unit_cost)", type="csv")
df = pd.read_csv(file if file else "data/sample_sales.csv", parse_dates=["date"])
if not file:
    st.sidebar.info("Using synthetic sample data. Upload your own CSV to replace it.")

service = st.sidebar.slider("Service level", 0.80, 0.99, 0.95, 0.01)
order_cost = st.sidebar.number_input("Ordering cost per order", 1.0, 100000.0, 500.0)
holding = st.sidebar.slider("Holding cost rate (of unit cost)", 0.05, 0.50, 0.20, 0.01)
lt = st.sidebar.number_input("Avg lead time (days)", 1, 120, 7)
lt_std = st.sidebar.number_input("Lead time std dev (days)", 0.0, 30.0, 1.5)

df["annual_value"] = df["units"] * df["unit_cost"]
tab1, tab2, tab3 = st.tabs(["ABC analysis", "Inventory policy", "Demand forecast"])

with tab1:
    abc = abc_classification(df)
    c1, c2 = st.columns(2)
    c1.dataframe(abc, use_container_width=True)
    c2.plotly_chart(px.bar(abc.groupby("abc_class", as_index=False)["annual_value"].sum(),
                           x="abc_class", y="annual_value", title="Value by class"),
                    use_container_width=True)

with tab2:
    st.dataframe(sku_policy_table(df, service, order_cost, holding, lt, lt_std),
                 use_container_width=True)

with tab3:
    sku = st.selectbox("SKU", sorted(df["sku"].unique()))
    method = st.radio("Method", ["Moving average", "Exponential smoothing"], horizontal=True)
    monthly = df[df["sku"] == sku].set_index("date")["units"].resample("MS").sum()
    f = (moving_average_forecast(monthly, 3) if method == "Moving average"
         else exponential_smoothing_forecast(monthly, 0.3))
    st.metric("MAPE (%)", f"{mape(monthly, f):.1f}")
    st.plotly_chart(px.line(pd.DataFrame({"Actual": monthly, "Forecast": f}), markers=True),
                    use_container_width=True)
