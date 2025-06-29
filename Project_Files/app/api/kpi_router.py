from fastapi import APIRouter, UploadFile, File
import pandas as pd
from io import StringIO
from sklearn.linear_model import LinearRegression
import numpy as np

router = APIRouter()

@router.post("/upload-kpi")
async def upload_kpi(file: UploadFile = File(...)):
    contents = await file.read()
    df = pd.read_csv(StringIO(contents.decode("utf-8")))

    if "Year" not in df.columns or "KPI" not in df.columns:
        return {"error": "CSV must contain 'Year' and 'KPI' columns"}

    X = df["Year"].values.reshape(-1, 1)
    y = df["KPI"].values

    model = LinearRegression()
    model.fit(X, y)

    next_year = max(df["Year"]) + 1
    predicted = model.predict(np.array([[next_year]]))[0]

    return {
        "forecast": {
            "next_year": int(next_year),
            "predicted_value": round(float(predicted), 2),
            "input_years": df["Year"].tolist(),
            "input_values": df["KPI"].tolist()
        }
    }
