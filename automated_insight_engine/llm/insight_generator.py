import os
import json
from dotenv import load_dotenv
import openai

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise EnvironmentError("OPENAI_API_KEY not set in environment")

openai.api_key = OPENAI_API_KEY


def _build_prompt(summary: dict) -> str:
    # Keep prompt compact and deterministic
    summary_json = json.dumps(summary, indent=2)
    prompt = (
        "You are a senior data analyst. Use only the dataset summary provided. "
        "Provide:\n"
        "1) Executive summary (2-3 sentences)\n"
        "2) Top 5 insights (bulleted)\n"
        "3) Anomalies or data quality concerns\n"
        "4) Suggested KPIs to track\n\n"
        "Dataset summary:\n"
        f"{summary_json}\n\n"
        "Respond in plain text with clear sections."
    )
    return prompt


def generate_insights(summary: dict, model: str = "gpt-4o-mini") -> str:
    prompt = _build_prompt(summary)
    resp = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a concise data analyst."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=600,
        temperature=0.0
    )
    # Defensive parsing
    choices = resp.get("choices", [])
    if not choices:
        return "No response returned from LLM."
    return choices[0].get("message", {}).get("content", "").strip()
