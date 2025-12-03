import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise EnvironmentError("GEMINI_API_KEY not set in .env")

# Configure Gemini client
genai.configure(api_key=api_key)

# USE CORRECT MODEL
MODEL_NAME = "models/gemini-2.5-flash"


def _build_prompt(summary: dict) -> str:
    summary_json = json.dumps(summary, indent=2)

    return (
        "You are a senior data analyst. Use ONLY the dataset summary provided.\n"
        "Return the following sections:\n"
        "1. Executive Summary (2–3 sentences)\n"
        "2. Top 5 Insights (bullet points)\n"
        "3. Any anomalies or data quality issues\n"
        "4. Suggested KPIs to monitor\n\n"
        f"Dataset Summary:\n{summary_json}\n"
    )


def generate_insights(summary: dict):
    prompt = _build_prompt(summary)
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as exc:
        return f"Failed to generate insights: {exc}"
