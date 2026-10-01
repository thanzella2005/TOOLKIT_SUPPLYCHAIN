"""Generate SYNTHETIC daily sales data for demo purposes (not real company data)."""
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)
dates = pd.date_range("2025-01-01", periods=365)
rows = []
for i in range(1, 31):
    base = rng.uniform(5, 120)
    cost = round(rng.uniform(50, 2000), 2)
    season = 1 + 0.2 * np.sin(np.arange(365) / 365 * 2 * np.pi * 2)
    units = np.maximum(0, rng.normal(base * season, base * 0.25)).round()
    rows += [(d, f"SKU{i:03d}", u, cost) for d, u in zip(dates, units)]
pd.DataFrame(rows, columns=["date", "sku", "units", "unit_cost"]).to_csv("data/sample_sales.csv", index=False)
print("Wrote data/sample_sales.csv")
