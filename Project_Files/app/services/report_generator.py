from app.services.granite_llm import ask_granite
from datetime import datetime
from pathlib import Path
from fpdf import FPDF

# 1. Generate Sustainability Report via Granite LLM
def generate_sustainability_report(content: str) -> str:
    prompt = (
        "You are a sustainability analyst. Based on the following document or metrics, "
        "generate a professional sustainability report suitable for smart city planners:\n\n"
        f"{content}\n\n"
        "Structure the report with clear headings like Summary, Challenges, Recommendations."
    )
    return ask_granite(prompt)

# 2. Save Markdown Report
def generate_markdown_report(summary: str) -> str:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"sustainability_report_{timestamp}.md"
    path = Path("app/data") / filename
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        f.write("# Sustainability Report\n\n")
        f.write(summary)
    
    return str(path)

# 3. Save PDF Report
def convert_to_pdf(summary: str) -> str:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"sustainability_report_{timestamp}.pdf"
    path = Path("app/data") / filename
    path.parent.mkdir(parents=True, exist_ok=True)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for line in summary.split("\n"):
        pdf.multi_cell(0, 10, line)

    pdf.output(str(path))
    return str(path)
