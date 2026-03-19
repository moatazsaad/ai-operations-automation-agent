# AI Operations Automation Agent

An end-to-end AI-powered system that automates business KPI reporting using LLMs, PostgreSQL, FastAPI, and Slack integration.

This project demonstrates how natural language requests can trigger real business workflows including data querying, report generation, approval flows, and automated delivery.

---

## 🚀 Overview

This system allows users to:

- Ask business questions in natural language
- Generate weekly KPI reports
- Automatically analyze company data from PostgreSQL
- Produce reports in Markdown and PDF formats
- Trigger workflows via Slack mentions
- Approve and upload reports directly in Slack
- Schedule automated weekly report delivery

---

## ⚙️ Features

- **AI Agent (LLM-powered)**  
  Converts natural language into structured tool calls

- **Database Analytics (PostgreSQL)**  
  Computes KPIs such as:
  - Total revenue
  - Top customers
  - Top products
  - Total orders
  - Average order value

- **Report Generation**
  - Markdown reports
  - PDF reports (via ReportLab)
  - Timestamped outputs

- **Slack Integration**
  - Trigger reports via bot mention
  - Approval-based workflow (`approve`)
  - PDF upload directly to Slack channel

- **FastAPI Service**
  - `/run-agent` → interact with agent
  - `/generate-report` → generate report directly
  - `/slack/events` → handle Slack events

- **Automation**
  - Weekly scheduled reports via cron

---

## 🏗️ Architecture

```

Slack / CLI / API
↓
FastAPI
↓
LLM Agent (LiteLLM)
↓
Tool Calling Layer
↓
PostgreSQL Database
↓
Report Generation (MD + PDF)
↓
Slack Delivery / File Output

```

---

## 📁 Project Structure

```

ai-operations-agent/
│
├── app/
│   ├── agent.py
│   ├── main.py
│   ├── run_agent.py
│   ├── run_weekly_report.py
│   ├── test_report_tool.py
│   │
│   ├── database/
│   │   ├── db.py
│   │   └── test_db.py
│   │
│   ├── tools/
│   │   ├── database_tools.py
│   │   ├── report_tools.py
│   │   ├── email_tools.py
│
├── reports/
├── requirements.txt
├── .gitignore
└── README.md

````

---

## 🛠️ Setup

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/ai-operations-automation-agent.git
cd ai-operations-automation-agent
````

### 2. Create virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file in the root:

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/ai_ops
SLACK_BOT_TOKEN=your_slack_token
SLACK_SIGNING_SECRET=your_slack_secret
```

---

## 🗄️ Database Setup

Create PostgreSQL database and tables:

```sql
CREATE DATABASE ai_ops;

CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    name TEXT,
    email TEXT
);

CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name TEXT,
    category TEXT,
    price NUMERIC
);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    customer_id INT,
    product_id INT,
    quantity INT,
    total_amount NUMERIC,
    order_date DATE,
    status TEXT
);
```

---

## ▶️ Running the Application

### Run FastAPI server

```bash
uvicorn app.main:app --reload
```

Open:

```
http://127.0.0.1:8000/docs
```

---

## 🧠 Using the Agent

### CLI

```bash
python -m app.run_agent "What is our total revenue?"
```

### API

POST `/run-agent`

```json
{
  "prompt": "Generate weekly sales report"
}
```

---

## 📊 Generate Report Directly

POST `/generate-report`

Response:

```json
{
  "message": "Weekly report generated successfully",
  "markdown_path": "...",
  "pdf_path": "..."
}
```

---

## 💬 Slack Usage

### Trigger report

```
@ai-ops-agent generate weekly KPI report
```

### Approve upload

```
approve
```

### Workflow

1. User requests report
2. System generates report
3. User approves
4. PDF uploaded to Slack

---

## ⏱️ Scheduled Automation (Cron)

Example weekly job:

```bash
0 9 * * MON cd /path/to/project && /path/to/.venv/bin/python -m app.run_weekly_report
```

---

## 📌 Key Design Decisions

* **Tool-based architecture** for modular AI workflows
* **Separation of fetch vs agent tools** for clean design
* **Approval-based Slack workflow** to prevent unintended actions
* **Rolling 7-day window** used for weekly reporting
* **In-memory event tracking** (can be upgraded to Redis in production)

---

## 🚧 Future Improvements

* Persistent storage for approvals and event tracking (Redis)
* Enhanced report formatting (charts, branding)
* Role-based Slack permissions
* Cloud deployment (AWS/GCP)
* Dashboard UI for report access

