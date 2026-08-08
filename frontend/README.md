# AI Procurement Control Tower - Frontend

A Next.js dashboard for procurement/inventory/supplier data, talking to the
FastAPI backend through read-only endpoints under `/api/metrics/*`.

Live at [https://aiops.moatazai.com](https://aiops.moatazai.com).

## Stack

Next.js (App Router, TypeScript) with `output: 'export'` (static export, no
Node server needed) + Tailwind CSS + shadcn/ui + Recharts + TanStack Query.

## Local development

Requires the FastAPI backend running locally first (from the repo root):

```bash
source .venv/bin/activate
# ALLOWED_ORIGINS in .env must include http://localhost:3000
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Then, in this directory:

```bash
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000). `.env.local` controls
which API the frontend calls (`NEXT_PUBLIC_API_BASE_URL`, defaults to
`http://localhost:8000`).

## Building

```bash
npm run build
```

Produces a static `out/` folder (HTML/CSS/JS, no server required).

## Deploying

Built with an empty `NEXT_PUBLIC_API_BASE_URL` (see `.env.production.local`)
so API calls resolve as relative paths - the frontend and API are served from
the same domain in production. The `out/` folder is copied to
`/var/www/aiops-frontend` on the EC2 box, and Nginx serves it directly at
`aiops.moatazai.com`, proxying `/api/metrics/*`, `/run-agent`, and
`/generate-operations-report` to FastAPI on `localhost:8000`.
