from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel
from ..services.report_generator import generate_sustainability_report, generate_markdown_report, convert_to_pdf

router = APIRouter()

class TextData(BaseModel):
    text: str

@router.post("/generate-report")
def generate_report(data: TextData):
    report = generate_sustainability_report(data.text)
    if report:
        return {"report": report}
    return {"report": None}

@router.post("/upload-txt-generate-markdown")
def upload_txt_to_markdown(file: UploadFile = File(...)):
    content = file.file.read().decode("utf-8")
    summary = generate_sustainability_report(content)
    path = generate_markdown_report(summary)
    return {"markdown": summary, "path": path}

@router.post("/upload-txt-generate-pdf")
def upload_txt_to_pdf(file: UploadFile = File(...)):
    content = file.file.read().decode("utf-8")
    summary = generate_sustainability_report(content)
    pdf_path = convert_to_pdf(summary)
    return {"summary": summary, "pdf_path": pdf_path}
