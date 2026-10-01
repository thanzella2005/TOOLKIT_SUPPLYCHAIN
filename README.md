# Supply Chain Analyst Toolkit

A Python toolkit and Streamlit dashboard for inventory analytics.

## Features
- ABC (Pareto) classification of SKUs
- EOQ, safety stock (service level, demand and lead-time variability) and reorder point
- Demand forecasting (moving average, exponential smoothing) with MAPE
- Interactive dashboard (Streamlit + Plotly)

## Setup
```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python generate_sample_data.py     # creates SYNTHETIC demo data
streamlit run app.py
pytest
```

## Data format
CSV with columns: `date, sku, units, unit_cost`.

## Note
The bundled sample data is synthetic and for demonstration only.
