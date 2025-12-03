import os
from flask import Flask, render_template, request, send_file, redirect, url_for, flash
from werkzeug.utils import secure_filename

from processors.file_detector import detect_file_type
from processors.data_processor import process_csv, process_sql, process_db
from llm.insight_generator import generate_insights
from reports.report_builder_pdf import create_pdf_report
from reports.report_builder_pptx import create_pptx_report

UPLOAD_FOLDER = "uploads"
REPORT_FOLDER = "generated_reports"
ALLOWED_EXTENSIONS = {"csv", "sql", "db", "sqlite"}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REPORT_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.secret_key = os.environ.get("FLASK_SECRET", "devsecret")


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    if "datafile" not in request.files:
        flash("No file part")
        return redirect(url_for("index"))

    file = request.files["datafile"]
    if file.filename == "":
        flash("No selected file")
        return redirect(url_for("index"))

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        saved_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(saved_path)

        ftype = detect_file_type(filename)
        try:
            if ftype == "csv":
                df, summary = process_csv(saved_path)
            elif ftype == "sql":
                df, summary = process_sql(saved_path)
            elif ftype == "db":
                df, summary = process_db(saved_path)
            else:
                flash("Unsupported file type detected")
                return redirect(url_for("index"))
        except Exception as exc:
            flash(f"Error processing file: {exc}")
            return redirect(url_for("index"))

        try:
            insights_text = generate_insights(summary)
        except Exception as exc:
            insights_text = f"Failed to generate insights: {exc}"

      
        base = os.path.splitext(filename)[0]
        pdf_path = os.path.join(REPORT_FOLDER, f"{base}.pdf")
        pptx_path = os.path.join(REPORT_FOLDER, f"{base}.pptx")

        #  reports
        try:
            create_pdf_report(summary, insights_text, pdf_path)
            create_pptx_report(summary, insights_text, pptx_path)
        except Exception as exc:
            flash(f"Failed to generate reports: {exc}")
            return redirect(url_for("index"))

        return render_template(
    "index.html",
    insights=insights_text,
    pdf_file=f"{base}.pdf",
    pptx_file=f"{base}.pptx",
    uploaded_file=filename
)


    flash("File not allowed")
    return redirect(url_for("index"))


@app.route("/download/<path:filename>")
def download(filename):
    safe_path = os.path.join(REPORT_FOLDER, secure_filename(filename))
    if os.path.exists(safe_path):
        return send_file(safe_path, as_attachment=True)
    flash("File not found")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
