from fastapi import APIRouter, UploadFile, File, Form
from services.anomaly_file_checker import detect_anomalies_from_csv

router = APIRouter()

@router.post("/check-anomalies", tags=["Anomaly Detection"])
async def check_anomalies(
    file: UploadFile = File(...),
    kpi: str = Form(...),
    threshold: float = Form(...)
):
    contents = await file.read()
    from io import StringIO
    csv_file = StringIO(contents.decode("utf-8"))

    try:
        result = detect_anomalies_from_csv(csv_file, kpi, threshold)
        print("🔍 Backend anomaly result:", result)
        return result
    except Exception as e:
        print("❌ Backend Error:", str(e))
        return {"anomalies": [], "error": str(e)}
