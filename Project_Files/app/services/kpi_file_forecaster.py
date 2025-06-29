# ✅ File: app/services/kpi_file_forecaster.py

import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

def forecast_kpi(df: pd.DataFrame):
    df.columns = [col.strip() for col in df.columns]
    if df.shape[1] < 2:
        return {"error": "CSV must have at least 2 columns"}

    years = df.iloc[:, 0].astype(int).values.reshape(-1, 1)
    values = df.iloc[:, 1].astype(float).values

    model = LinearRegression()
    model.fit(years, values)

    next_year = int(years[-1][0]) + 1
    prediction = model.predict(np.array([[next_year]]))[0]

    return {
        "input_years": years.flatten().tolist(),
        "input_values": values.tolist(),
        "next_year": next_year,
        "predicted_value": round(float(prediction), 2)
    }
