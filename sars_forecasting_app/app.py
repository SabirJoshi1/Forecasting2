```python
import streamlit as st
import numpy as np
import pandas as pd
from data.loader import load_data
from logic.preprocessing import apply_filters
from logic.forecasting import train_arimax_model
from utils.kpi import calculate_kpis, compute_inventory
from config.style import inject_style
import plotly.graph_objs as go

st.set_page_config(page_title="SARS Forecasting Platform", layout="wide")
inject_style()

st.title("📊 SARS Forecasting Platform")

uploaded_file = st.file_uploader("📁 Upload your Last Year Sales File", type=["csv"])
if not uploaded_file:
    st.warning("⚠️ Please upload a CSV file to proceed.")
    st.stop()

raw_df = load_data(uploaded_file)

# Layout: Filters on right, content on left
left_col, right_col = st.columns([3, 1])

with right_col:
    st.markdown("### 🔎 Filter Options")
    region = st.selectbox("🌍 Region", sorted(raw_df['Region_Code'].unique()))
    store_type = st.selectbox("🏪 Store Type", sorted(raw_df['Store_Type'].unique()))
    location = st.selectbox("📍 Location Type", sorted(raw_df['Location_Type'].unique()))

filtered_df = apply_filters(raw_df, region, store_type, location)

# Aggregate data
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

tab1, tab2 = st.tabs(["📈 Dashboard", "📁 Download"])

with tab1:
    with left_col:
        st.subheader("🔢 Key Performance Indicators")
        kpi_df = pd.DataFrame({
            'KPI': ['Total Forecast Period', 'Avg Forecasted Sales', 'Validation RMSE'],
            'Value': [f"{len(val_dates)} days", f"${forecast.mean():,.0f}", f"${rmse:,.0f}"]
        })
        st.dataframe(kpi_df)

        st.subheader("📉 Forecast vs Actual Sales")
        chart_df = pd.DataFrame({'Actual Sales': actual.values, 'Forecasted Sales': forecast.values}, index=val_dates)
        st.line_chart(chart_df)

        st.subheader("📦 Inventory Recommendation Table")
        inventory_df = pd.DataFrame({
            'Date': val_dates,
            'Forecasted Sales': forecast.values,
            'Recommended Stock Level': recommended_stock.values,
            'Safety Stock': safety_stock
        })
        st.dataframe(inventory_df.style.format({
            "Forecasted Sales": "{:.0f}",
            "Recommended Stock Level": "{:.0f}",
            "Safety Stock": "{:.0f}"
        }))

        st.subheader("📈 Inventory Level vs Forecast Chart")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=val_dates, y=forecast, mode='lines', name='Forecasted Sales'))
        fig.add_trace(go.Scatter(x=val_dates, y=recommended_stock, mode='lines', name='Recommended Stock Level'))
        fig.update_layout(title='Forecast vs Inventory Level', xaxis_title='Date', yaxis_title='Units')
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.download_button("Download Forecast Table (CSV)",
                       chart_df.reset_index().to_csv(index=False).encode(),
                       "forecast_data.csv", "text/csv")

    st.download_button("Download Inventory Plan (CSV)",
                       inventory_df.reset_index().to_csv(index=False).encode(),
                       "inventory_plan.csv", "text/csv")
```
