
# AI Operations Automation Agent

![Project Overview](assets/project_overview.png)

AI-powered operations and procurement automation platform built with FastAPI, PostgreSQL, MCP tools, Slack workflows, scheduled reporting, and a Streamlit dashboard.

The system helps teams monitor business performance, procurement risks, supplier performance, inventory shortages, reorder needs, and executive reports through both APIs and natural language AI prompts.

---

## Project Overview

This project started as an AI sales KPI reporting agent and was extended into a procurement and supply chain intelligence platform.

It can:

- Answer business KPI questions using live PostgreSQL data
- Detect low-stock inventory items
- Recommend reorder quantities
- Detect delayed purchase orders automatically
- Analyze supplier performance
- Analyze procurement spend by supplier
- Generate weekly sales/KPI reports
- Generate weekly operations/procurement reports
- Upload scheduled reports to Slack
- Provide a Streamlit procurement dashboard
- Use MCP tools to connect the AI agent to backend functions

---

## Business Value

In a real enterprise, this system would sit on top of ERP/MRP systems such as SAP, Oracle, Coupa, or Microsoft Dynamics.

The AI layer does not replace ERP. It adds intelligence on top of operational data by helping managers quickly answer questions like:

- Which suppliers are causing delays?
- Which items need reorder?
- Where is procurement spend highest?
- Which purchase orders are delayed?
- What are the current inventory risks?
- What should be prioritized this week?

---

## Main Features

### 1. Sales KPI Analytics

The agent can calculate:

- Total revenue
- Total completed orders
- Average order value
- Top customers
- Top products

Example prompts:

```text
What is total revenue?
Show top customers.
Generate weekly sales report.
````

---

### 2. Inventory Risk Monitoring

The system detects low-stock items using:

```text
current_stock <= reorder_point
```

Example prompt:

```text
Show low stock items.
```

---

### 3. Reorder Recommendations

The system recommends reorder quantities using:

```text
recommended_order_quantity = reorder_point + safety_stock - current_stock
```

Example prompt:

```text
Show reorder recommendations.
```

---

### 4. Delayed Purchase Order Detection

The system automatically detects delayed POs using:

```text
actual_delivery_date IS NULL
AND expected_delivery_date < CURRENT_DATE
```

Example prompt:

```text
Which purchase orders are delayed?
```

---

### 5. Supplier Performance Analytics

The system calculates:

* Total purchase orders
* Delayed purchase orders
* Delivered purchase orders
* On-time deliveries
* On-time delivery rate
* Total supplier spend

Example prompt:

```text
Show supplier performance.
```

---

### 6. Procurement Spend Analysis

The system calculates supplier spend using:

```text
SUM(total_amount) GROUP BY supplier
```

Example prompt:

```text
Show procurement spend by supplier.
```

---

### 7. Operations Report Generation

The system generates a weekly operations report including:

* Inventory risks
* Low-stock items
* Delayed purchase orders
* Supplier performance
* Procurement spend by supplier

Outputs:

```text
Markdown report
PDF report
```

Example prompt:

```text
Generate weekly operations report.
```

---

### 8. Slack Automation

The system can upload reports to Slack automatically.

Current Slack capabilities:

* Scheduled weekly report upload
* Report file upload
* Slack bot integration
* Slack signature verification
* Approval-ready workflow structure

---

### 9. Streamlit Dashboard

The project includes a Streamlit dashboard called:

```text
AI Procurement Control Tower
```

Dashboard sections:

* Executive KPI cards
* AI insights
* Recommended actions
* Spend by supplier chart
* Supplier on-time delivery chart
* Delayed PO chart
* Inventory risk chart
* Detailed procurement tables
* Report generation button

Run with:

```bash
.venv/bin/python -m streamlit run app/dashboard.py
```

---

## Tech Stack

* Python
* FastAPI
* PostgreSQL
* psycopg2
* Pydantic
* MCP
* OpenAI Agents SDK
* LiteLLM
* Fireworks AI / LLM endpoint
* Slack SDK
* ReportLab
* Streamlit
* Pandas
* Cron jobs

---

## Project Structure

```text
app/
├── agent.py
├── main.py
├── mcp_server.py
├── dashboard.py
├── run_weekly_report.py
├── run_weekly_operations_report.py
│
├── database/
│   └── db.py
│
├── services/
│   ├── metrics_service.py
│   ├── procurement_metrics_service.py
│   ├── report_service.py
│   ├── operations_report_service.py
│   ├── email_service.py
│   └── slack_service.py
│
reports/
├── weekly_sales_report_*.md
├── weekly_sales_report_*.pdf
├── weekly_operations_report_*.md
└── weekly_operations_report_*.pdf
```

---

## Database Tables

Existing sales tables:

```text
customers
orders
products
```

Procurement and supply chain tables:

```text
suppliers
purchase_orders
inventory
```

---

## Environment Variables

Create a `.env` file:

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/ai_ops
SLACK_BOT_TOKEN=your_slack_bot_token
SLACK_SIGNING_SECRET=your_slack_signing_secret
```

---

## Run the FastAPI App

```bash
uvicorn app.main:app --reload --port 8001
```

API docs:

```text
http://127.0.0.1:8001/docs
```

---

## Important API Endpoints

Health check:

```bash
GET /
```

Run AI agent:

```bash
POST /run-agent
```

Generate sales report:

```bash
POST /generate-report
```

Generate operations report:

```bash
POST /generate-operations-report
```

Slack events endpoint:

```bash
POST /slack/events
```

---

## Example API Calls

Run agent:

```bash
curl -s -X POST http://127.0.0.1:8001/run-agent \
-H "Content-Type: application/json" \
-d '{"prompt":"Show supplier performance"}'
```

Generate operations report:

```bash
curl -s -X POST http://127.0.0.1:8001/generate-operations-report
```

Show reorder recommendations:

```bash
curl -s -X POST http://127.0.0.1:8001/run-agent \
-H "Content-Type: application/json" \
-d '{"prompt":"Show reorder recommendations"}'
```

---

## Run Streamlit Dashboard

```bash
.venv/bin/python -m streamlit run app/dashboard.py
```

Open:

```text
http://127.0.0.1:8501
```

---

## Scheduled Weekly Operations Report

Cron job example:

```bash
0 9 * * MON cd /home/moataz/projects/ai-operations-automation-agent && /home/moataz/.local/bin/uv run python -m app.run_weekly_operations_report >> cron.log 2>&1
```

This runs every Monday at 9 AM and uploads the weekly operations report to Slack.

---

## MCP Tools

The AI agent uses MCP tools such as:

```text
get_total_revenue
get_top_customers
get_top_products
get_total_orders
get_average_order_value
get_low_stock_items
get_delayed_purchase_orders
get_supplier_performance
get_procurement_spend_by_supplier
get_reorder_recommendations
generate_sales_report
generate_operations_report
draft_sales_report_email
```

---

## Example Manager Workflow

1. The system receives procurement and inventory data.
2. It detects low stock, delayed POs, supplier issues, and spend concentration.
3. It generates a weekly operations report.
4. The manager receives the PDF in Slack.
5. The manager asks the AI agent follow-up questions.
6. The manager takes action in SAP/ERP.

Example actions:

* Follow up with delayed supplier
* Approve replenishment
* Escalate delayed PO
* Review supplier scorecard
* Prioritize urgent purchases

---

## Enterprise Positioning

This project demonstrates how AI agents can be used as an operations intelligence layer on top of ERP/MRP systems.

It combines:

* Procurement domain knowledge
* AI agents
* SQL analytics
* MCP tool architecture
* Slack automation
* Scheduled reporting
* Dashboard visualization
* Executive decision support

---

## Future Improvements

Planned improvements:

* Authentication and user roles
* Persistent approval storage using PostgreSQL or Redis
* Supplier risk scoring
* Spend by category
* Open PO aging
* Lead time analytics
* ERP/SAP API integration
* AI chat inside Streamlit dashboard
* More advanced forecasting
* Cloud deployment

---

## Summary

This project is an AI-powered procurement and operations control tower.

It helps organizations move from manual reporting and scattered ERP checks to automated risk detection, supplier visibility, inventory intelligence, and executive-ready reporting.



