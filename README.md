# AI Operations Automation Agent

![Project Overview](assets/project_overview.png)

**Live Application:** https://aiops.moatazai.com  

AI-powered procurement and operations control tower that lets managers ask business questions in plain English and receive KPI, supplier, inventory, spend, risk, and reporting insights from operational data.

The platform combines **FastAPI**, **PostgreSQL**, **Next.js**, **MCP tools**, **LLM agent orchestration**, **Slack workflows**, scheduled reporting, and a production-style AWS deployment with **Nginx**, **HTTPS**, and secured internal ports.

---

## Project Summary

This project started as an AI sales KPI reporting agent and evolved into a procurement and operations intelligence platform.

It helps managers answer questions such as:

- Which purchase orders are delayed?
- Which suppliers have the worst delivery performance?
- Which inventory items need reorder?
- Where is procurement spend concentrated?
- What operational risks should be prioritized this week?
- Can I generate a weekly executive operations report?

Instead of manually checking spreadsheets, dashboards, or ERP screens, users can interact with the system through a web dashboard, API endpoints, Slack workflows, and natural-language AI prompts.

---

## Live Production-Style Deployment

The application is deployed on AWS EC2 and available at:

```text
https://aiops.moatazai.com
```

Production-style deployment work completed:

- Deployed FastAPI backend and a Next.js frontend (static export) on AWS EC2
- Configured a `systemd` service so FastAPI restarts after crashes or EC2 reboot
- Added Nginx reverse proxy so users access the app through a standard web URL
- Attached an Elastic IP for a stable public server address
- Connected Cloudflare DNS using `aiops.moatazai.com`
- Enabled HTTPS/SSL for secure browser access
- Closed direct public access to the internal app port `8000`
- Kept traffic routed through Nginx as the public entry point

Production flow:

```text
User
  ↓
https://aiops.moatazai.com
  ↓
Cloudflare DNS
  ↓
AWS Elastic IP
  ↓
Nginx reverse proxy
  ↓
Next.js static frontend (Nginx serves it directly)  +  FastAPI backend on localhost:8000
  ↓
PostgreSQL database on localhost:5432
```

---

# Business Problem

In a real enterprise, this system can sit on top of ERP/MRP systems such as SAP, Oracle, Coupa, or Microsoft Dynamics.

The AI layer does not replace ERP systems. It adds an intelligence and automation layer that helps business users:

- Detect procurement risks faster
- Identify low-stock inventory items
- Track delayed supplier deliveries
- Generate weekly executive reports
- Ask operational questions without writing SQL
- Turn raw operational data into recommended actions

---

## Key Features

### Natural-Language AI Agent

Managers can ask questions such as:

```text
Show me delayed purchase orders.
Show me low-stock items.
Which suppliers have the worst delays?
Generate weekly operations report.
```

The FastAPI backend receives the prompt, routes it to the LLM agent, calls the correct tool or service, queries PostgreSQL, and returns a business-ready response.

---

### Procurement and Inventory Analytics

The system supports:

- Low-stock detection
- Reorder recommendations
- Delayed purchase order tracking
- Supplier performance analysis
- Supplier spend analysis
- Inventory risk monitoring
- Weekly operations reporting

Example logic:

```text
Low stock:
current_stock <= reorder_point

Reorder recommendation:
recommended_order_quantity = reorder_point + safety_stock - current_stock

Delayed purchase order:
actual_delivery_date IS NULL
AND expected_delivery_date < CURRENT_DATE
```

---

### Frontend: AI Procurement Control Tower

A Next.js dashboard (`frontend/`) - TypeScript, Tailwind CSS, shadcn/ui, Recharts, TanStack Query - gives managers a visual control tower for procurement and operations.

Dashboard sections include:

- Executive KPI cards
- AI-generated insights
- Recommended actions
- Spend by supplier chart
- Supplier on-time delivery chart
- Delayed purchase order chart
- Inventory risk chart
- Detailed procurement tables
- Weekly report generation button
- Natural-language question box connected to FastAPI

---

### Slack Integration

The project includes Slack workflow support for operations reporting.

Slack capabilities include:

- Slack bot integration
- Scheduled weekly report delivery
- Report file uploads
- Slack signing secret verification
- Approval-ready workflow structure
- Notification workflow for generated reports

This allows managers to receive reports and operational updates directly inside Slack.

---

### Report Generation

The system generates executive-ready reports in:

```text
Markdown
PDF
```

Reports include:

- Inventory risks
- Low-stock items
- Delayed purchase orders
- Supplier performance
- Procurement spend
- Recommended actions

---

## Architecture

```text
Next.js Frontend
        ↓
FastAPI Backend
        ↓
LLM Agent / MCP Tools
        ↓
Python Service Layer
        ↓
PostgreSQL Database
        ↓
Markdown / PDF Reports
        ↓
Slack Notifications
```

The frontend uses read-only endpoints under `/api/metrics/*` (`app/routers/metrics.py`) instead of calling the service layer directly.

Deployment architecture:

```text
Cloudflare DNS
  ↓
AWS Elastic IP
  ↓
Nginx :80/:443
  ↓
Next.js static files (served directly by Nginx)  +  FastAPI :8000
  ↓
PostgreSQL :5432
```

---

# Infrastructure and DevOps

## AWS EC2 Deployment

The system is deployed on AWS EC2 using Ubuntu Linux.

Production setup includes:

* FastAPI backend service
* Next.js frontend (static export, served by Nginx)
* PostgreSQL database
* Nginx reverse proxy
* HTTPS SSL certificates
* Elastic IP
* Cloudflare-managed DNS
* CloudWatch monitoring

---

## systemd Services

FastAPI runs as a systemd service (the frontend is static files, served directly by Nginx - no process needed).

Benefits:

* Automatic restart after crashes
* Auto-start on server reboot
* Centralized logs
* Easier production management

Example service:

```text
fastapi.service
```

---

## Nginx Reverse Proxy

Nginx routes requests based on URL path.

Routing logic:

```text
https://aiops.moatazai.com
→ Next.js static files (served directly by Nginx)

https://aiops.moatazai.com/api/metrics/*
https://aiops.moatazai.com/run-agent
https://aiops.moatazai.com/generate-operations-report
https://aiops.moatazai.com/slack/events
→ FastAPI :8000
```

Benefits:

* One secure HTTPS domain
* Internal app ports remain private
* Cleaner production architecture
* Slack webhook support
* HTTPS termination

---

## HTTPS and Security

HTTPS was configured using Certbot and Let's Encrypt.

Security improvements include:

* SSL/TLS encryption
* Protected internal ports
* Slack signature verification
* HMAC verification for Slack events
* Timestamp validation to reduce replay attacks

Port `8000` is not exposed publicly.

---

## CloudWatch Monitoring

CloudWatch monitoring tracks:

* CPU utilization
* EC2 health status
* Network traffic
* Server activity

This helps monitor application health and server usage.

---

# Tech Stack

- **Languages:** Python, SQL
- **Backend:** FastAPI, Pydantic
- **Database:** PostgreSQL, psycopg2
- **AI/Agents:** LLM agents, MCP tools, LiteLLM, Fireworks AI endpoint
- **Frontend:** Next.js, TypeScript, Tailwind CSS, shadcn/ui, Recharts, TanStack Query, Framer Motion
- **Reports:** ReportLab, Markdown, PDF
- **Automation:** Scheduled jobs, Slack SDK
- **Deployment:** AWS EC2, Ubuntu, systemd, Nginx
- **Networking/Security:** Elastic IP, Cloudflare DNS, HTTPS/SSL, secured internal ports

---

# MCP Tool Architecture

The AI agent uses MCP tools such as:

```text
get_total_revenue
get_top_customers
get_total_orders
get_average_order_value
get_low_stock_items
get_delayed_purchase_orders
get_supplier_performance
get_procurement_spend_by_supplier
get_reorder_recommendations
generate_sales_report
generate_operations_report
```

MCP was used instead of simple decorated functions to create a cleaner separation between the agent and business tools.

Benefits include:

* Reusable tools
* Better modularity
* Easier debugging
* More scalable architecture
* Better enterprise-style design

---

# Project Structure

```text
app/
├── agent.py
├── main.py
├── mcp_server.py
├── run_agent.py
├── run_weekly_report.py
├── run_weekly_operations_report.py
│
├── routers/
│   └── metrics.py          # read-only REST endpoints for the frontend
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
frontend/                     # Next.js dashboard (live at aiops.moatazai.com)
├── src/
│   ├── app/                  # page, layout, providers
│   ├── components/dashboard/ # KPI cards, charts, tabs, ask-agent panel, etc.
│   ├── lib/                  # API client, types, palette, derived-text logic
│   └── hooks/                # TanStack Query hooks
│
reports/
├── weekly_sales_report_*.md
├── weekly_sales_report_*.pdf
├── weekly_operations_report_*.md
└── weekly_operations_report_*.pdf
```

---

## Database Tables

Sales and KPI tables:

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

Create a `.env` file in the project root.

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/ai_ops
SLACK_BOT_TOKEN=your_slack_bot_token
SLACK_SIGNING_SECRET=your_slack_signing_secret
OPENAI_API_KEY=your_openai_or_llm_key
HF_TOKEN=your_huggingface_token
ALLOWED_ORIGINS=http://localhost:3000
APP_API_KEY=a_random_secret_string
```

`ALLOWED_ORIGINS` is a comma-separated CORS allow-list, only needed when the frontend runs on a different origin than the API (e.g. local dev). In production both are served from the same domain, so it has no effect there.

`APP_API_KEY` protects `/run-agent`, `/generate-operations-report`, `/generate-report`, and `/api/metrics/*` behind an `X-API-Key` header, so only requests carrying this key go through. The frontend sends it automatically (`NEXT_PUBLIC_API_KEY` in its own env file).

Do not commit `.env` to GitHub.

---

## Local Setup

Clone the repository:

```bash
git clone https://github.com/moatazsaad/ai-operations-automation-agent.git
cd ai-operations-automation-agent
```

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Start FastAPI:

```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

FastAPI docs:

```text
http://127.0.0.1:8000/docs
```

Start the Next.js frontend (needs FastAPI running first, with `ALLOWED_ORIGINS` including `http://localhost:3000`):

```bash
cd frontend
npm install
npm run dev
```

```text
http://localhost:3000
```

---

## Important API Endpoints

Health check:

```text
GET /
```

Run AI agent:

```text
POST /run-agent
```

Generate sales report:

```text
POST /generate-report
```

Generate operations report:

```text
POST /generate-operations-report
```

Slack events endpoint:

```text
POST /slack/events
```

Read-only metrics endpoints (new - used by the Next.js frontend):

```text
GET /api/metrics/low-stock-items
GET /api/metrics/delayed-purchase-orders
GET /api/metrics/supplier-performance
GET /api/metrics/spend-by-supplier
GET /api/metrics/reorder-recommendations
GET /api/metrics/top-delayed-suppliers
```

Report file endpoint (serves a generated report so the frontend can show it inline - no API key needed, only the exact generated filename works):

```text
GET /reports/{filename}
```

---

## Example API Calls

Run the agent:

```bash
curl -X POST http://127.0.0.1:8000/run-agent \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Show supplier performance"}'
```

Generate operations report:

```bash
curl -X POST http://127.0.0.1:8000/generate-operations-report
```

Show reorder recommendations:

```bash
curl -X POST http://127.0.0.1:8000/run-agent \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Show reorder recommendations"}'
```

---

## Production Service Management

FastAPI is managed with `systemd`. The frontend is static files served directly by Nginx, so there's no frontend process to manage.

Check service status:

```bash
sudo systemctl status fastapi
sudo systemctl status nginx
```

Restart services:

```bash
sudo systemctl restart fastapi
sudo systemctl reload nginx
```

View logs:

```bash
sudo journalctl -u fastapi -f
sudo journalctl -u nginx -f
```

---

## Scheduled Weekly Operations Report

Example scheduled workflow:

```bash
0 9 * * MON cd /home/ubuntu/ai-operations-automation-agent && /home/ubuntu/ai-operations-automation-agent/venv/bin/python -m app.run_weekly_operations_report >> cron.log 2>&1
```

This runs every Monday at 9 AM and can generate/upload the weekly operations report to Slack.

---

## MCP Tools

The AI agent can use tools such as:

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
send_slack_report_notification
```

---

## Example Manager Workflow

1. Procurement and inventory data are stored in PostgreSQL.
2. The system detects low stock, delayed purchase orders, supplier risks, and spend concentration.
3. A manager opens the dashboard or asks the AI agent a natural-language question.
4. The agent calls the correct backend tools and returns insights.
5. The system generates a weekly Markdown/PDF operations report.
6. Slack workflows deliver reports or notifications to the team.
7. Managers use the insights to follow up with suppliers, approve replenishment, or escalate delays.

---

## Security and Production Notes

Completed:

- Deployed the application on AWS EC2 with Ubuntu Linux
- Configured FastAPI as a `systemd` service for automatic restart after crashes or server reboot
- Deployed the Next.js frontend as a static export, served directly by Nginx
- Added Nginx as a reverse proxy and single public entry point
- Connected Cloudflare DNS to the EC2 Elastic IP using `aiops.moatazai.com`
- Enabled HTTPS/SSL using Certbot and Let's Encrypt
- Removed direct public access to the internal app port `8000`
- Routed `/slack/events` through Nginx to FastAPI for Slack webhook handling
- Added Slack signature verification using HMAC and timestamp checks
- Added basic CloudWatch monitoring for CPU utilization, EC2 instance health checks, and NetworkIn/NetworkOut traffic

Planned:

- Add user authentication and role-based access control
- Store database backups outside EC2 using S3 or migrate PostgreSQL to RDS with automated backups
- Move secrets from `.env` to AWS Secrets Manager or Parameter Store
- Add CloudWatch alarms and deeper disk/log monitoring using CloudWatch Agent
- Add user activity logging to track prompts, report generation, and Slack workflow actions

---

## Future Improvements

- Authentication and role-based access control
- Persistent approval storage using PostgreSQL or Redis
- Supplier risk scoring
- Spend by category analytics
- Open purchase order aging
- Lead time analytics
- ERP/SAP API integration
- AI chat history inside the dashboard
- Inventory demand forecasting
- Automated database backups to S3
- CloudWatch alarms, disk monitoring, and centralized application logs

---
