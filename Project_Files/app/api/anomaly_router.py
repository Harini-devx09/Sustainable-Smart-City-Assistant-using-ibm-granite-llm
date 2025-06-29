from fastapi import APIRouter, UploadFile, File, Form, HTTPException
import pandas as pd

router = APIRouter()

@router.post("/check-anomalies")
async def check_anomalies(kpi: str = Form(...), threshold: float = Form(...), file: UploadFile = File(...)):
    try:
        df = pd.read_csv(file.file)
        if kpi not in df.columns:
            raise HTTPException(status_code=400, detail=f"KPI column '{kpi}' not found in file")

        anomalies = df[df[kpi] > threshold]
        return {
            "anomalies": anomalies.to_dict(orient="records")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
