from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from app.services.granite_llm import ask_granite
import tempfile
from fpdf import FPDF

router = APIRouter()

class ReportTextRequest(BaseModel):
    text: str

@router.post("/generate-report")
def generate_report(request: ReportTextRequest):
    prompt = f"Generate a sustainability report for the following data:\n{request.text}"
    try:
        response = ask_granite(prompt)
        return {"report": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/upload-txt-generate-pdf")
def upload_txt_generate_pdf(file: UploadFile = File(...)):
    try:
        content = file.file.read().decode("utf-8")
        prompt = f"Generate a sustainability report from this data:\n{content}"
        summary = ask_granite(prompt)

        # Generate PDF from summary
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        for line in summary.split('\n'):
            pdf.multi_cell(0, 10, line)

        temp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        pdf.output(temp.name)

        return {
            "summary": summary,
            "pdf_path": temp.name
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process file: {e}")
