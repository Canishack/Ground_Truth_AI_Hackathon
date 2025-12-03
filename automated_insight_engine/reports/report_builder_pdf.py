from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER
import datetime
from typing import Dict
import textwrap


def create_pdf_report(summary: Dict, insights: str, output_path: str):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40,
    )

    styles = getSampleStyleSheet()
    story = []

    # Title
    title_style = styles["Title"]
    title_style.alignment = TA_CENTER
    story.append(Paragraph("Automated Insight Engine Report", title_style))
    story.append(Spacer(1, 12))

    # Timestamp
    timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    story.append(Paragraph(f"<i>Generated: {timestamp}</i>", styles["Normal"]))
    story.append(Spacer(1, 20))

    # -------------------- Dataset Overview Section --------------------
    story.append(Paragraph("<b>1. Dataset Overview</b>", styles["Heading2"]))
    story.append(Spacer(1, 8))

    overview_data = [
        ["Metric", "Value"],
        ["Rows", summary.get("row_count")],
        ["Columns", len(summary.get("columns", []))],
    ]

    t = Table(overview_data, hAlign="LEFT")
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e8e8e8")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 6),
                ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
                ("GRID", (0, 0), (-1, -1), 0.3, colors.gray),
            ]
        )
    )

    story.append(t)
    story.append(Spacer(1, 18))

    # -------------------- Missing Values Table --------------------
    story.append(Paragraph("<b>2. Missing Values</b>", styles["Heading2"]))
    story.append(Spacer(1, 8))

    mv = summary.get("missing_values", {})
    mv_data = [["Column", "Missing Count"]]

    for col, val in mv.items():
        mv_data.append([col, val])

    mv_table = Table(mv_data, hAlign="LEFT")
    mv_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e8e8e8")),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("GRID", (0, 0), (-1, -1), 0.3, colors.gray),
                ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
            ]
        )
    )

    story.append(mv_table)
    story.append(Spacer(1, 18))

    # -------------------- AI Insights Section --------------------
    story.append(Paragraph("<b>3. AI Insights</b>", styles["Heading2"]))
    story.append(Spacer(1, 10))

    wrapped = "<br/>".join(textwrap.wrap(insights, width=110))
    story.append(Paragraph(wrapped, styles["BodyText"]))
    story.append(Spacer(1, 24))

    # -------------------- Sample Rows Table --------------------
    story.append(Paragraph("<b>4. Sample Rows</b>", styles["Heading2"]))
    story.append(Spacer(1, 8))

    sample = summary.get("sample_rows", [])
    if sample:
        # Header
        headers = list(sample[0].keys())
        rows = [headers]

        for row in sample:
            rows.append([str(row[col]) for col in headers])

        sample_table = Table(rows, hAlign="LEFT")
        sample_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e8e8e8")),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("GRID", (0, 0), (-1, -1), 0.3, colors.gray),
                    ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
                ]
            )
        )

        story.append(sample_table)

    doc.build(story)
