from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import textwrap
import datetime
from typing import Dict


def _wrap(text: str, width: int = 90):
    lines = []
    for paragraph in text.splitlines():
        lines.extend(textwrap.wrap(paragraph, width=width) or [""])
    return lines


def create_pdf_report(summary: Dict, insights: str, output_path: str):
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter
    margin = 50
    y = height - margin

    c.setFont("Helvetica-Bold", 16)
    c.drawString(margin, y, "Automated Insight Engine")
    y -= 24
    c.setFont("Helvetica", 9)
    c.drawString(margin, y, f"Generated: {datetime.datetime.utcnow().isoformat()} UTC")
    y -= 18

    # Overview
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin, y, "Dataset Overview")
    y -= 16
    c.setFont("Helvetica", 9)
    c.drawString(margin, y, f"Rows: {summary.get('row_count')}, Columns: {len(summary.get('columns', []))}")
    y -= 14

    # Missing values
    c.setFont("Helvetica-Bold", 10)
    c.drawString(margin, y, "Missing values (per column):")
    y -= 14
    c.setFont("Helvetica", 9)
    missing = summary.get("missing_values", {})
    for k, v in missing.items():
        c.drawString(margin + 8, y, f"{k}: {v}")
        y -= 12
        if y < 80:
            c.showPage()
            y = height - margin

    c.showPage()
    y = height - margin
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin, y, "AI Insights")
    y -= 18
    c.setFont("Helvetica", 10)
    for line in _wrap(insights, width=95):
        c.drawString(margin, y, line)
        y -= 12
        if y < 60:
            c.showPage()
            y = height - margin
            c.setFont("Helvetica", 10)

    c.showPage()
    y = height - margin
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin, y, "Sample Rows")
    y -= 18
    c.setFont("Helvetica", 9)
    sample = summary.get("sample_rows", [])
    for row in sample:
        s = ", ".join(f"{k}={v}" for k, v in row.items())
        for line in textwrap.wrap(s, width=110):
            c.drawString(margin, y, line)
            y -= 12
            if y < 60:
                c.showPage()
                y = height - margin

    c.save()
