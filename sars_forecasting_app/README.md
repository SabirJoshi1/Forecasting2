# SARS Forecasting Platform

This Streamlit app provides ARIMAX-based sales forecasting for SARS data, helping optimize inventory and reduce stockouts.

## 📦 Features

- Upload historical sales data (`.csv`)
- Apply filters by region, store type, and location
- Train ARIMAX model on filtered data
- Visualize forecast vs actual sales
- Generate KPIs and inventory recommendations

## ▶️ How to Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## 🌐 Deploy on Streamlit Cloud

Ensure these files are in your GitHub repo:

- `app.py`
- `requirements.txt`
- `config/`, `data/`, `logic/`, `utils/` folders

Then link the repo to [streamlit.io](https://streamlit.io) and deploy!

## 📁 Example CSV Format

The uploaded file should include columns:

- `Date` (e.g. 2024-01-01)
- `Sales`, `Holiday`, `#Order`, `Discount`, `Store_id`, `Region_Code`, `Store_Type`, `Location_Type`