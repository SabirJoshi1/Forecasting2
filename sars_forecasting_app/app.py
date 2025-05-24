import streamlit as st
import numpy as np
import pandas as pd
from data.loader import load_data
from logic.preprocessing import apply_filters
from logic.forecasting import train_arimax_model
from utils.kpi import calculate_kpis, compute_inventory
from config.style import inject_style

st.set_page_config(page_title="SARS Forecasting Platform", layout="wide")
inject_style()

st.markdown("## 📊 SARS Forecasting Platform")

uploaded_file = st.file_uploader("📁 Upload your Last Year Sales File", type=["csv"])
if not uploaded_file:
    st.warning("⚠️ Please upload a CSV file to proceed.")
    st.stop()

raw_df = load_data(uploaded_file)

region = st.selectbox("Region", sorted(raw_df['Region_Code'].unique()))
store_type = st.selectbox("Store Type", sorted(raw_df['Store_Type'].unique()))
location = st.selectbox("Location Type", sorted(raw_df['Location_Type'].unique()))

filtered_df = apply_filters(raw_df, region, store_type, location)

# Aggregate and prepare data
df = filtered_df.groupby('Date').agg({
    'Sales': 'sum',
    'Holiday': 'max',
    '#Order': 'sum',
    'Discount': 'sum',
    'Store_id': 'nunique'
}).asfreq('D').fillna(method='ffill')
df['Date'] = df.index

latest_year = df.last('365D')
latest_year['log_sales'] = np.log1p(latest_year['Sales'])

log_sales_series = latest_year['log_sales']
exog = latest_year[['Holiday', '#Order', 'Discount', 'Store_id']]

forecast_log, val_y, _, train_end, val_end = train_arimax_model(log_sales_series, exog)
forecast, actual, rmse = calculate_kpis(forecast_log, val_y)
safety_stock, recommended_stock = compute_inventory(forecast)

val_dates = latest_year.index[train_end:val_end]
st.line_chart(pd.DataFrame({'Actual': actual.values, 'Forecast': forecast.values}, index=val_dates))