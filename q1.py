import sqlite3
import pandas as pd
from scipy.stats import pearsonr
import json

# Load SQL script
with open("q-sql-correlation-github-pages.sql", "r") as file:
    sql_script = file.read()

# Load data into in-memory SQLite DB
conn = sqlite3.connect(":memory:")
cursor = conn.cursor()
cursor.executescript(sql_script)

# List available tables
tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';", conn)
print("Tables in DB:\n", tables)

# Replace 'your_table_name' with the actual table name found above
df = pd.read_sql("SELECT * FROM retail_data", conn)

# Compute correlations
corr1, _ = pearsonr(df["Footfall"], df["Net_Sales"])
corr2, _ = pearsonr(df["Footfall"], df["Returns"])
corr3, _ = pearsonr(df["Net_Sales"], df["Returns"])

correlations = {
    "Footfall-Net_Sales": corr1,
    "Footfall-Returns": corr2,
    "Net_Sales-Returns": corr3
}

# Find the strongest correlation by absolute value
strongest_pair = max(correlations.items(), key=lambda x: abs(x[1]))

# Save result
result = {
    "pair": strongest_pair[0],
    "correlation": round(strongest_pair[1], 3)
}

with open("result.json", "w") as f:
    json.dump(result, f)

print("Strongest correlation:", result)