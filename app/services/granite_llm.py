import os
import io
import traceback
from dotenv import load_dotenv
from pydantic import SecretStr
from langchain_ibm import WatsonxLLM
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from fpdf import FPDF



# Load environment variables
load_dotenv()



# Define the required environment variables
required_env_vars = [
    "WATSONX_MODEL_ID",
    "WATSONX_PROJECT_ID",
    "WATSONX_URL",
    "WATSONX_API_KEY"
]

# Load and validate all
env = {var: os.getenv(var) for var in required_env_vars}

# Check if any are missing
missing = [key for key, value in env.items() if not value]
if missing:
    raise EnvironmentError(f"Missing required environment variables: {', '.join(missing)}")

# Optional fallback for backwards compatibility
if not env["WATSONX_API_KEY"]:
    alt_key = os.getenv("WATSONXAPIKEY")
    if alt_key:
        env["WATSONX_API_KEY"] = alt_key
    else:
        raise EnvironmentError("Missing WATSONX_API_KEY or WATSONXAPIKEY")

# Assign them to variables
model_id = env["WATSONX_MODEL_ID"]
project_id = env["WATSONX_PROJECT_ID"]
url = env["WATSONX_URL"]
apikey = env["WATSONX_API_KEY"]


# Initialize Watsonx LLM
watsonx_llm = WatsonxLLM(
    model_id=os.getenv("WATSONX_MODEL_ID"),
    url=os.getenv("WATSONX_URL"),
    apikey=os.getenv("WATSONX_API_KEY"),
    project_id=os.getenv("WATSONX_PROJECT_ID"),
    params={"decoding_method": "greedy", "max_new_tokens": 1024}, # Increase timeout if needed
)

# Prompt wrapper
def create_chain(template: str):
    prompt = PromptTemplate.from_template(template)
    return LLMChain(prompt=prompt, llm=watsonx_llm)

# 1. 🔹 Chat Assistant
def ask_granite(prompt: str) -> str:
    try:
        print("🔍 Prompt sent to Granite:\n", prompt)
        chain = create_chain("{question}")
        result = chain.invoke({"question": prompt})
        print("🧠 Granite Response:\n", result['text'])
        return result['text']
    except Exception as e:
        print("🔥 Granite Error:\n", traceback.format_exc())
        return None

# 2. 📄 Policy Summarizer
def generate_summary(text: str) -> str:
    prompt = f"""Summarize the following city policy document clearly for a citizen:\n\n{text}"""
    return ask_granite(prompt)

# 3. 🌿 Eco Tip Generator
def generate_eco_tip(topic: str) -> str:
    prompt = f"Provide 5 practical eco-friendly tips related to the topic: {topic}. Keep it concise and bullet-pointed."
    result = watsonx_llm.invoke(prompt)
    return result.content if hasattr(result, "content") else str(result)

# 4. 📈 City KPI Sustainability Report
def generate_city_report(kpi_data: str) -> str:
    prompt = f"""Based on the following KPI data, write a detailed smart city sustainability report:\n\n{kpi_data}"""
    return ask_granite(prompt)

# 5. 📘 Sustainability Report Generator
def generate_sustainability_report(content: str) -> str:
    prompt = (
        "You are a sustainability analyst. Based on the following document or metrics, "
        "generate a concise sustainability report suitable for city planners: \n\n"
        f"{content}\n\n"
        "Structure the report with clear headings like Summary, Challenges, Recommendations."
    )
    return ask_granite(prompt)

# 6. 🧾 Markdown Report for Sustainability
def generate_markdown_report(summary: str) -> str:
    markdown = "# Sustainability Report\n\n"
    markdown += summary
    return markdown

def generate_pdf_report(text: str) -> bytes:
    """
    Generates a professional-looking PDF from given text content.
    Returns PDF as bytes (to be sent as HTTP response or saved to file).
    """
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
    
    lines = text.split("\n")
    for line in lines:
        pdf.multi_cell(0, 10, line)

    pdf_output = io.BytesIO()
    pdf.output(pdf_output)
    return pdf_output.getvalue()