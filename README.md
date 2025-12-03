# 🚀 Automated Insight Engine  
**Tagline:** A web-based intelligence system that transforms raw CSV/SQL/DB files into clean structured data, AI-generated insights, and export-ready PDF/PPTX reports — all in under 10 seconds.

---

# 1. 🎯 The Problem — Real-World Motivation  
While working on data-heavy projects, I observed a recurring pain point:  
**Most analysts spend too much time cleaning data, running ad-hoc summaries, and formatting reports manually.**

###  The Real Issues:
- Raw CSV/SQL dumps are messy  
- Pandas profiling takes time  
- Insights aren’t always obvious  
- Creating PDF/PPT reports is boring  
- Stakeholders need answers *fast*, not in hours  

### 💡 My Solution  
I built the **Automated Insight Engine**, a lightweight, web-based AI system where:

👉 The user uploads a raw file  
👉 The system processes & analyzes it  
👉 And instantly returns:  
- Cleaned dataset metadata  
- Missing values & descriptive stats  
- GPT-driven narrative insights  
- Ready-to-download **PDF & PPTX reports**

No coding. No manual cleaning. No waiting.

---

# 2. 🏁 Expected End Result

### For the User:

#### **Input**  
Upload any of the following:  
- `.csv`  
- `.sql`  
- `.db` / `.sqlite`

#### **Action**  
Click “Upload & Process”

#### **Output (Instant)**  
-  Clean summary (schema, stats, NA count)  
-  AI-generated insights (trends, anomalies, KPIs)  
-  Downloadable PDF  
- Downloadable PPTX deck  
-  Executive-ready content  

All generated dynamically using Python + OpenAI GPT.

---

# 3. 🧪 Technical Approach — Turning Raw Data Into Intelligence

I set out to build more than a script. I wanted a **mini production-grade intelligence engine**.

###  **1. File Detection**
A custom parser detects file type automatically:
- CSV → Pandas  
- SQL → Parsed into SQLite memory DB  
- DB/SQLite → Loaded directly via SQLAlchemy  

This ensures a **unified DataFrame** regardless of source.

---

### **2. Data Processing**
I implemented a structured ETL-like process:

- Column extraction  
- Schema inference  
- Missing value computation  
- `.describe()` numeric summary  
- First 5 sample rows  

This ensures the AI always receives clean, structured context.

---

###  **3. AI Insight Generation** *(The “Analyst”)*

The cleaned summary is passed to **GPT-4o-mini**, with a crafted prompt asking for:

1. Executive Summary  
2. Key Insights  
3. Anomalies  
4. KPI Suggestions  

This turns raw data → narrative business intelligence.

---

### 📝 **4. Report Generation**
I built two separate exporters:

- **PDF**: Generated via *ReportLab*  
- **PPTX**: Created using *python-pptx*  

Both include:
- Title  
- Metadata  
- Summary Stats  
- AI Narrative  
- Sample Data Rows  

Perfect for business users.

---

### 🌐 **5. Web Interface (Flask)**
A simple HTML/CSS UI allows:
- File upload  
- Viewing AI output  
- Downloading reports  

Fast, clean, minimal.

---

# 4.  Tech Stack

| Layer | Technology |
|-------|------------|
| **Frontend** | HTML, CSS |
| **Backend** | Python, Flask |
| **Data Engine** | Pandas, SQLAlchemy |
| **AI Engine** | OpenAI GPT-4o / GPT-4o-mini |
| **PDF Export** | ReportLab |
| **PPT Export** | python-pptx |
| **Config** | python-dotenv |
| **Storage** | Local temp storage (`uploads/`, `generated_reports/`) |

---

# 5.  Challenges & Learnings  

### **Challenge 1: Handling Different File Types**
CSV → fine.  
SQL dumps → messy.  
SQLite DBs → inconsistent schemas.

**Solution:**  
I built a custom file detector and a unified loader pipeline to convert everything → DataFrame.

---

### **Challenge 2: Keeping AI Outputs Grounded**
LLMs sometimes guess trends that don’t exist.

**Solution:**  
I constrained GPT’s responses using:
- Strict JSON summaries  
- Reinforced instructions (“Only use data provided”)  
- Zero temperature  

This dramatically reduced hallucinations.

---


# 7. ▶️ How to Run Locally  

```bash
# 1. Clone Repository
git clone https://github.com/Canishack/Ground_Truth_AI_Hackathon
cd Ground_Truth_AI_Hackathon/automated_insight_engine

# 2. Create Virtual Environment
python -m venv venv

# Activate:
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 3. Install Dependencies
pip install -r requirements.txt

# 4. Add API Key
echo "OPENAI_API_KEY=your_key_here" > .env

# 5. Run Server
python app.py


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
