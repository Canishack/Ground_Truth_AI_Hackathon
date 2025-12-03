# 📊 Automated Insight Engine  
> A lightweight, intelligent web application that converts **raw uploaded datasets** (CSV / SQL / DB files) into **clean formatted file, AI-generated insights, and downloadable PDF/PPTX reports**.  
This system uses **Python, Pandas, Flask & Generative AI** to transform unstructured data into **executive-ready intelligence**.

---

## ✨ Features  

- 📤 **Multi-Format Upload** – Supports `.csv`, `.sql`, `.db`, `.sqlite` files  
- 🔍 **Auto File-Type Detection** – Smart parser identifies the correct loader  
- 📊 **Automated Data Processing** – Schema extraction, statistics, missing values  
- 🧠 **AI  Insights** – GPT- generates trends, anomalies & KPIs  
- 📄 **PDF & PPTX Export** – Beautifully formatted reports for decision-makers  
- 🌐 **Web-Based Interface** – Clean upload page built with Flask + HTML  

---

## 🛠️ Tech Stack  

| Layer             | Technology |
|-------------------|------------|
| **Frontend**      | HTML, CSS  |
| **Backend**       | Python, Flask |
| **Data Processing** | Pandas, SQLAlchemy |
| **AI Engine**     | OpenAI GPT |
| **Report Export** | ReportLab (PDF), python-pptx (PPTX) |
| **Environment**   | python-dotenv |
| **Storage**       | Temporary file storage (`/uploads`, `/generated_reports`) |

---

## 📂 Project Structure  

```bash
automated_insight_engine/
├── app.py                     # Flask web server
├── requirements.txt           # Dependencies
├── .env                       # OpenAI API key
│
├── templates/
│   └── index.html             # Main upload UI
│
├── static/
│   └── style.css              # Minimal styling
│
├── processors/
│   ├── data_processor.py      # Data cleaning + stats
│   ├── file_detector.py       # Detect file type
│   └── db_reader.py           # Load SQL/DB files
│
├── llm/
│   └── insight_generator.py   # GPT-based narrative generation
│
├── reports/
│   ├── report_builder_pdf.py  # PDF generator
│   └── report_builder_pptx.py # PPT generator
│
├── uploads/                   # Raw uploaded files
└── generated_reports/         # Final downloadable reports

# ⚙️ Local Development
##🔑 Prerequisites

-Python 3.10+
-pip
-OpenAI API Key
-Virtual environment 

1️⃣ Clone Repository
git clone https://github.com/Canishack/Ground_Truth_AI_Hackathon
cd Ground_Truth_AI_Hackathon/automated_insight_engine

2️⃣ Create Virtual Environment
python -m venv venv


Activate:
Windows
venv\Scripts\activate


Mac/Linux
source venv/bin/activate

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Configure API Key
Create .env:
OPENAI_API_KEY=YOUR_OPENAI_KEY

5️⃣ Run Application
python app.py

App opens at:
👉 http://localhost:5000

You can now upload .csv, .sql, .db files → and download AI-generated PDF/PPTX reports.

🧠 How It Works (Pipeline)
1️⃣ User Uploads File
Stored in /uploads/.

2️⃣ File Detector Module
Identifies type:
CSV → read with Pandas
SQL Dump → parsed & loaded
DB/SQLite → loaded via SQLAlchemy


3️⃣ Data Processing Module
Generate schema
Compute numeric statistics
Identify missing values
Provide 5 sample rows

4️⃣ AI Insight Engine
Summary → GPT-4o → Output:
Executive summary
Key insights
Trends
Anomalies
KPI suggestions

5️⃣ Report Builder
User chooses:
PDF (ReportLab)
PPTX (python-pptx)
6️⃣ Download Final Report
Saved inside /generated_reports/.


📄 License
This project is licensed under the MIT License.