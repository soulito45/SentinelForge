# RYNEX

RYNEX is a locally hosted attack-surface intelligence and risk monitoring platform built for security analysts, researchers, and developers who want a practical way to discover exposed assets, track changes over time, and prioritize what matters most.

It combines discovery, exposure mapping, vulnerability detection, historical state tracking, and a lightweight dashboard into one workflow.

> Current verified status: the backend, API, dashboard build, and end-to-end scan flow are working in this workspace.

## Why RYNEX?

Most scanning tools stop at raw output. RYNEX goes one step further:

- it stores asset state across scans,
- compares current results to previous scans,
- detects changes in assets, ports, technologies, and findings,
- calculates an internal risk score to help prioritize investigation.

This makes RYNEX useful as both a portfolio project and a defensive security monitoring tool for authorized environments.

## Key Features

- Domain-based scan workflow with allowlist protection
- Subdomain discovery and DNS/IP resolution
- Nmap-based port and service exposure mapping
- HTTPX-based technology and web exposure detection
- Nuclei-based vulnerability/finding ingestion
- Historical change detection across scans
- Internal risk scoring for prioritization
- Dashboard for viewing assets, findings, and scan history
- Async scan execution through the FastAPI backend

## Architecture

```text
Analyst / UI
    ↓
FastAPI REST API
    ↓
Scan Orchestrator
    ├── Subfinder    → Subdomains
    ├── DNS Resolver → IPs / Hostnames
    ├── Nmap         → Ports / Services
    ├── HTTPX        → HTTP exposure / Technologies
    ├── Nuclei       → Findings / Vulnerabilities
    └── Change Engine → Asset / Port / Tech / Finding diffs
            ↓
      Risk Engine
            ↓
      PostgreSQL
```

## Tech Stack

### Backend
- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic

### Security Tools
- Subfinder
- Nmap
- HTTPX
- Nuclei

### Frontend
- React
- Vite
- JavaScript / JSX

## Verified Project Status

The following have been validated successfully in this workspace:

- `pytest -q` → `4 passed`
- `npm run build` in `dashboard/` → successful production build
- `GET /health` → healthy API response
- `GET /scans/` → valid scan history endpoint
- End-to-end scan on `scanme.nmap.org` → completed successfully

## Repository Structure

```text
RYNEX/
├── backend/
│   ├── app/
│   ├── api/
│   ├── core/
│   ├── models/
│   ├── schemas/
│   └── services/
├── dashboard/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── vite.config.js
├── risk/
├── scanner/
├── tests/
├── .env
├── requirements.txt
├── README.md
└── ...
```

## Quick Start

### Prerequisites

- Linux or WSL environment
- Python 3.x
- PostgreSQL
- Nmap
- Subfinder
- HTTPX
- Nuclei

### 1) Clone the repository

```bash
git clone <repository-url>
cd RYNEX
```

### 2) Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3) Install Python dependencies

```bash
pip install -r requirements.txt
```

### 4) Configure environment variables

Create a `.env` file with your PostgreSQL URL and allowed domains.

Example:

```env
DATABASE_URL=postgresql+psycopg2://USER:PASSWORD@localhost:5432/rynex
ALLOWED_DOMAINS=scanme.nmap.org
```

### 5) Start the backend

```bash
./.venv/bin/python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000
```

API endpoints will be available at:

- http://127.0.0.1:8000
- Swagger docs: http://127.0.0.1:8000/docs

### 6) Start the dashboard

```bash
cd dashboard
npm install
npm run dev
```

The dashboard will run on the Vite local development server, typically at:

- http://127.0.0.1:5173

## Basic Workflow

### Add a domain

```bash
curl -X POST 'http://127.0.0.1:8000/domains/?name=scanme.nmap.org'
```

### Start a scan

```bash
curl -X POST 'http://127.0.0.1:8000/scans/?domain_id=1'
```

### View scan history

```bash
curl http://127.0.0.1:8000/scans/
```

## How the Platform Thinks

RYNEX is designed around persistent attack-surface state.

Instead of showing a one-time scanner dump, it stores discovered data and continuously compares future scans against previous results.

That allows it to answer questions like:

- What new assets appeared?
- Which ports closed or reopened?
- What technologies changed?
- Which findings are new or resolved?
- What should be investigated first?

## Risk Model

RYNEX currently uses an internal prioritization model rather than raw CVSS scoring.

It combines indicators such as:

- finding severity,
- internet-facing exposure,
- web exposure,
- SSH exposure,
- database exposure,
- detected service versions.

The goal is operational prioritization, not formal vulnerability scoring.

## Security and Ethics

RYNEX is intended for authorized environments only.

Do not scan:

- third-party infrastructure,
- client or employer systems without explicit authorization,
- arbitrary internet targets outside your permitted scope.

This project is meant for defensive security research, learning, and portfolio development.

## Current Limitations

This project is a working local MVP with the following scope:

- local owner-controlled usage,
- dashboard connected to live API data,
- async scan execution through the API,
- domain allowlist enforcement,
- internal risk prioritization rather than external CVSS scoring.

## Roadmap

### Completed
- FastAPI backend
- PostgreSQL integration
- Domain management
- Asset discovery
- DNS and IP tracking
- Nmap port mapping
- HTTPX detection
- Nuclei findings ingestion
- Change detection
- Risk scoring
- Dashboard integration
- Local verification and hardening

### Planned
- Better search/filtering in the dashboard
- Improved scanner failure handling
- More polished logging and validation
- Additional reporting and analytics views
- Scheduled scanning support
- Authentication and RBAC

## Project Status Summary

RYNEX is now in a strong working state as a locally hosted, analyst-oriented security platform for authorized attack-surface monitoring.

It has been validated for:

- backend startup,
- API health and scan endpoints,
- frontend build,
- domain allowlist enforcement,
- end-to-end scanning with a safe public test domain.

## Contributing

Contributions are welcome. If you want to improve the project:

1. open an issue,
2. create a feature branch,
3. make a clean pull request,
4. include verification details.

## Disclaimer

RYNEX is an educational, defensive-security project. Use it only against systems you own or are explicitly authorized to test.
