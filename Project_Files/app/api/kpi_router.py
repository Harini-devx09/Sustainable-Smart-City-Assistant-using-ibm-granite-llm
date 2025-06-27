from fastapi import APIRouter

router = APIRouter()

@router.get("/kpi-metrics", tags=["KPI Metrics"])
def get_sample_kpi():
    # Sample static KPI metrics
    return {
        "water_usage": "123 ML",
        "energy_consumption": "4000 kWh",
        "air_quality_index": "72"
    }
