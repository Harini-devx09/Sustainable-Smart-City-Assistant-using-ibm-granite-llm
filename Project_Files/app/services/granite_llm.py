import os
import io
import traceback
from langchain_ibm import WatsonxLLM
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from fpdf import FPDF

# Only load .env if it exists (for local development)
if os.path.exists(".env"):
    from dotenv import load_dotenv
    load_dotenv()


# Define required environment variables
required_env_vars = [
    "WATSONX_MODEL_ID",
    "WATSONX_PROJECT_ID",
    "WATSONX_URL",
    "WATSONX_API_KEY"
]

# Load and validate all required env vars
env = {var: os.getenv(var) for var in required_env_vars}
missing = [key for key, value in env.items() if not value]
if missing:
    raise EnvironmentError(f"Missing required environment variables: {', '.join(missing)}")

# Optional fallback for older key naming (if needed)
if not env["WATSONX_API_KEY"]:
    alt_key = os.getenv("WATSONXAPIKEY")
    if alt_key:
        env["WATSONX_API_KEY"] = alt_key
    else:
        raise EnvironmentError("Missing WATSONX_API_KEY or WATSONXAPIKEY")

# Assign to variables
model_id = env["WATSONX_MODEL_ID"]
project_id = env["WATSONX_PROJECT_ID"]
url = env["WATSONX_URL"]
apikey = env["WATSONX_API_KEY"]

# Initialize Watsonx LLM client
watsonx_llm = WatsonxLLM(
    model_id=model_id,
    url=url,
    apikey=apikey,
    project_id=project_id,
    params={"decoding_method": "greedy", "max_new_tokens": 1024},
)

# Helper to create prompt chains
def create_chain(template: str):
    prompt = PromptTemplate.from_template(template)
    return LLMChain(prompt=prompt, llm=watsonx_llm)

# 1. Chat assistant query
def ask_granite(prompt: str) -> str:
    try:
        print("🔍 Prompt sent to Granite:\n", prompt)
        chain = create_chain("{question}")
        result = chain.invoke({"question": prompt})
        print("🧠 Granite Response:\n", result['text'])
        return result['text']
    except Exception:
        print("🔥 Granite Error:\n", traceback.format_exc())
        return None

# 2. Policy summarizer
def generate_summary(text: str) -> str:
    prompt = f"Summarize the following city policy document clearly for a citizen:\n\n{text}"
    return ask_granite(prompt)

# 3. Eco tip generator
def generate_eco_tip(prompt: str) -> str:
    result = watsonx_llm.invoke(prompt)
    return result.content if hasattr(result, "content") else str(result)


# 4. City KPI sustainability report
def generate_city_report(kpi_data: str) -> str:
    prompt = f"Based on the following KPI data, write a detailed smart city sustainability report:\n\n{kpi_data}"
    return ask_granite(prompt)

# 5. Sustainability report generator
def generate_sustainability_report(content: str) -> str:
    prompt = (
        "You are a sustainability analyst. Based on the following document or metrics, "
        "generate a concise sustainability report suitable for city planners:\n\n"
        f"{content}\n\n"
        "Structure the report with clear headings like Summary, Challenges, Recommendations."
    )
    return ask_granite(prompt)

# 6. Markdown report generator
def generate_markdown_report(summary: str) -> str:
    markdown = "# Sustainability Report\n\n"
    markdown += summary
    return markdown

# 7. PDF report generator
def generate_pdf_report(text: str) -> bytes:
    class PDF(FPDF):
        def header(self):
            self.set_font("Arial", "B", 14)
            self.cell(0, 10, "Smart City Sustainability Report", ln=True, align="C")
            self.ln(5)

        def footer(self):
            self.set_y(-15)
            self.set_font("Arial", "I", 8)
            self.cell(0, 10, f"Page {self.page_no()}", align="C")

    pdf = PDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    for line in text.split("\n"):
        pdf.multi_cell(0, 10, line)

    pdf_output = io.BytesIO()
    pdf.output(pdf_output)
    return pdf_output.getvalue()
