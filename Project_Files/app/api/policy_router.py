# app/api/policy_router.py

from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel
from app.services.granite_llm import (
    generate_summary, generate_markdown_report, generate_city_report, generate_pdf_report
)



router = APIRouter(prefix="/policy", tags=["Policy Summarizer"])

class TextData(BaseModel):
    text: str

@router.post("/summarize-policy")
def summarize_policy(data: TextData):
    summary = generate_summary(data.text)
    return {"summary": summary}

@router.post("/summarize-uploaded-file")
async def summarize_uploaded_file(file: UploadFile = File(...)):
    content = (await file.read()).decode("utf-8")
    summary = generate_summary(content)
    return {"summary": summary}

@router.get("/summarize-from-file")
def summarize_from_file():
    try:
        with open("samplepolicy.txt", "r", encoding="utf-8") as f:
            content = f.read()
        summary = generate_summary(content)
        return {"summary": summary}
    except Exception as e:
        return {"error": str(e)}

@router.post("/generate-report")
def generate_ai_report(data: TextData):
    report = generate_city_report(data.text)
    return {"report": report}

@router.post("/generate-markdown-report")
def generate_markdown(data: TextData):
    markdown = generate_markdown_report(data.text)
    return {"markdown": markdown}

@router.post("/generate-pdf-report")
def generate_pdf(data: TextData):
    pdf_bytes = generate_pdf_report(data.text)
    return {"pdf": pdf_bytes}

@router.post("/upload-txt-generate-markdown")
async def upload_txt_to_markdown(file: UploadFile = File(...)):
    content = (await file.read()).decode("utf-8")
    markdown = generate_markdown_report(content)
    return {"markdown": markdown}

@router.post("/upload-txt-generate-pdf")
async def upload_txt_to_pdf(file: UploadFile = File(...)):
    content = (await file.read()).decode("utf-8")
    pdf_bytes = generate_pdf_report(content)
    return {"pdf": pdf_bytes}

@router.get("/test-11m")
def test_llm():
    try:
        result = generate_summary("Test connection to Watsonx Granite")
        return {"status": "✅ Connected", "sample": result}
    except Exception as e:
        return {"status": "❌ Failed", "error": str(e)}
