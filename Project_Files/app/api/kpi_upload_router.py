# ✅ File: app/api/kpi_upload_router.py

from fastapi import APIRouter, UploadFile, File
import pandas as pd
from app.services.kpi_file_forecaster import forecast_kpi

router = APIRouter()

@router.post("/upload-kpi", tags=["KPI Upload"])
async def upload_kpi_csv(file: UploadFile = File(...)):
    df = pd.read_csv(file.file)
    prediction = forecast_kpi(df)
    return {"forecast": prediction}
