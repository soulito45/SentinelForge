# 🛡️ RYNEX

### External Attack Surface Intelligence & Risk Monitoring Platform

RYNEX is a locally hosted cybersecurity platform designed to discover, map, monitor, and prioritize internet-facing attack-surface exposure.

Instead of treating vulnerability scanning as a one-time activity, RYNEX maintains an evolving view of assets, ports, technologies, findings, risk, and security changes across scans.

> **Current status:** Day 5 of 7 — Core backend, scanning pipeline, risk engine, and change detection completed.
> **Dashboard and final project hardening are planned for Days 6–7.**

---

## 🎯 Project Goal

The goal of RYNEX is to answer a practical security question:

> **"What is exposed, what changed, and what should I investigate first?"**

The platform combines multiple security tools into a structured monitoring pipeline:

```text
Authorized Domain
       ↓
Subdomain Discovery
       ↓
DNS / IP Resolution
       ↓
Nmap
       ↓
HTTPX
       ↓
Nuclei
       ↓
Normalization
       ↓
Change Detection
       ↓
Risk Engine
       ↓
PostgreSQL
       ↓
FastAPI API
```

The project is intentionally designed around **asset state and historical change**, rather than simply displaying raw scanner output.

---

# 🔥 Why RYNEX?

Traditional scanner workflows often produce large amounts of output without answering:

* What assets are currently exposed?
* Which assets appeared or disappeared?
* Which ports opened or closed?
* Which technologies changed?
* Which findings are new?
* Which findings were resolved?
* Which exposed asset deserves attention first?

RYNEX attempts to provide that context by maintaining state between scans.

### Core differentiator

```text
Scanner Output
      ↓
Structured Asset State
      ↓
Historical Comparison
      ↓
Security Changes
      ↓
Contextual Risk
      ↓
Analyst Prioritization
```

This makes RYNEX more than a basic Nmap/Nuclei wrapper.

---

# 🏗️ Architecture

```text
                    ┌─────────────────────┐
                    │      Analyst        │
                    │   / API Consumer    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │      FastAPI        │
                    │       REST API      │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Scan Orchestrator │
                    └──────────┬──────────┘
                               │
             ┌─────────────────┼─────────────────┐
             ▼                 ▼                 ▼
       ┌──────────┐      ┌──────────┐      ┌──────────┐
       │ Subfinder│      │   Nmap   │      │  HTTPX   │
       └────┬─────┘      └────┬─────┘      └────┬─────┘
            │                 │                 │
            ▼                 ▼                 ▼
       Subdomains           Ports         HTTP / Tech
            │                 │                 │
            └─────────────────┼─────────────────┘
                              ▼
                         ┌─────────┐
                         │ Nuclei  │
                         └────┬────┘
                              │
                              ▼
                         Findings
                              │
                              ▼
                  ┌──────────────────────┐
                  │   Change Detection   │
                  └──────────┬───────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │     Risk Engine      │
                  └──────────┬───────────┘
                             │
                             ▼
                     ┌──────────────┐
                     │  PostgreSQL  │
                     └──────────────┘
```

---

# 🧰 Technology Stack

## Backend

* Python
* FastAPI
* SQLAlchemy
* PostgreSQL
* Pydantic / environment configuration

## Security Tooling

* Subfinder
* Nmap
* ProjectDiscovery HTTPX
* Nuclei

## Planned Frontend

* React / Next.js
* Analyst-focused security dashboard

> The dashboard is **not yet implemented** as of Day 5.

---

# 📊 Current Project Status

| Component                   | Status     |
| --------------------------- | ---------- |
| Project foundation          | ✅ Complete |
| FastAPI backend             | ✅ Complete |
| PostgreSQL integration      | ✅ Complete |
| Domain management           | ✅ Complete |
| Asset discovery             | ✅ Complete |
| DNS/IP resolution           | ✅ Complete |
| Nmap integration            | ✅ Complete |
| Port tracking               | ✅ Complete |
| HTTPX integration           | ✅ Complete |
| Technology tracking         | ✅ Complete |
| Nuclei integration          | ✅ Complete |
| Finding lifecycle           | ✅ Complete |
| Risk engine                 | ✅ Complete |
| Asset risk calculation      | ✅ Complete |
| Asset change detection      | ✅ Complete |
| Port change detection       | ✅ Complete |
| Technology change detection | ✅ Complete |
| Finding change detection    | ✅ Complete |
| Full scan orchestration     | ✅ Complete |
| End-to-end pipeline         | ✅ Complete |
| Security dashboard          | 🚧 Day 6   |
| Final testing/hardening     | 🚧 Day 7   |
| Documentation polish        | 🚧 Day 7   |
| GitHub portfolio polish     | 🚧 Day 7   |

---

# 🔍 Core Capabilities

## 1. Asset Discovery

RYNEX uses Subfinder to discover subdomains associated with an authorized domain.

Discovered hostnames are:

* Normalized
* Deduplicated
* DNS resolved
* Stored as assets
* Associated with IP addresses
* Tracked using `first_seen` and `last_seen`

### Asset lifecycle

```text
New Asset
   ↓
ACTIVE
   ↓
Not discovered
   ↓
INACTIVE
```

Historical asset records are retained.

---

# 🌐 2. Exposure Mapping

Nmap is used to identify exposed network services.

RYNEX extracts:

* Port number
* Protocol
* State
* Service
* Product
* Version

Example:

```text
5432/tcp → PostgreSQL
8000/tcp → HTTP / Uvicorn
```

Ports are retained historically rather than being deleted when they disappear.

---

# 🕸️ 3. HTTP & Technology Mapping

ProjectDiscovery HTTPX identifies HTTP/HTTPS exposure and technology information.

Collected information includes:

* HTTP URL
* Status code
* Page title
* Web server
* Technologies
* Host/IP information

Technology lifecycle is tracked using:

```text
ACTIVE
INACTIVE
```

Historical technology records are retained.

---

# 🔎 4. Vulnerability Detection

Nuclei is integrated into the pipeline for vulnerability and exposure detection.

RYNEX stores:

* Template ID
* Finding title
* Severity
* Evidence
* Matched location
* Asset
* Scan
* First seen
* Last seen
* Status

Finding lifecycle:

```text
NEW
 ↓
OPEN
 ↓
RESOLVED
```

Repeated findings are deduplicated using the asset and Nuclei template relationship.

---

# ⚠️ 5. Contextual Risk Engine

RYNEX calculates an internal prioritization score using finding severity and exposure context.

Factors currently considered include:

* Finding severity
* Internet-facing status
* Web exposure
* SSH exposure
* Database exposure
* Detected service version

Risk levels:

```text
LOW
MEDIUM
HIGH
CRITICAL
```

### Important

The RYNEX score is an **internal prioritization score**.

It is **not CVSS** and should not be interpreted as an official vulnerability severity standard.

---

# 🔄 6. Change Detection

One of RYNEX's primary features is comparing security state between scans.

### Asset changes

* New asset
* Removed asset

### Port changes

* New open port
* Closed port

### Technology changes

* New technology
* Removed technology

### Finding changes

* New finding
* Resolved finding

Every detected change can retain:

* Change type
* Description
* Previous value
* Current value
* Asset
* Scan
* Detection timestamp

Example:

```text
Previous Scan
22/tcp → OPEN

Current Scan
22/tcp → CLOSED

RYNEX
↓
CLOSED_PORT
```

---

# 🧠 State Tracking

RYNEX is designed around persistent security state.

Instead of:

```text
Scan → Output → Throw output away
```

the platform follows:

```text
Scan
 ↓
Store State
 ↓
Next Scan
 ↓
Compare State
 ↓
Detect Change
 ↓
Update State
 ↓
Calculate Risk
```

This allows the system to evolve toward continuous attack-surface monitoring.

---

# 🗄️ Database Model

Current core entities:

```text
Domain
  │
  └── Asset
        │
        ├── IPAddress
        ├── Port
        ├── Technology
        └── Finding

Scan
  │
  ├── Finding
  └── Change

Asset
  │
  └── Change
```

Core tables:

* `domains`
* `assets`
* `ip_addresses`
* `ports`
* `technologies`
* `findings`
* `scans`
* `changes`

---

# 🧪 Current End-to-End Pipeline

The complete backend pipeline has been successfully tested locally:

```text
Domain
  ↓
Discovery
  ↓
Asset
  ↓
Nmap
  ↓
Ports
  ↓
HTTPX
  ↓
Technologies
  ↓
Nuclei
  ↓
Findings
  ↓
Change Detection
  ↓
Risk Calculation
  ↓
PostgreSQL
  ↓
FastAPI
```

Repeated scans with no environmental changes correctly produce:

```text
Asset changes:       0
Port changes:        0
Technology changes:  0
Finding changes:     0
Total changes:       0
```

The system has also successfully detected actual port-state changes during controlled testing.

---

# 🧪 Local Test Environment

Development and integration testing is performed locally.

Example test asset:

```text
test.rynex.local
```

Example observed state:

```text
22/tcp    closed
443/tcp   closed
5432/tcp  open
8000/tcp  open
```

Technologies:

```text
Python
Uvicorn
```

Example finding:

```text
swagger-api
Severity: info
Status: open
```

Current local test data exists only to validate the platform's functionality.

---

# 🚀 Installation

## Requirements

* Linux
* Python 3.x
* PostgreSQL
* Nmap
* Subfinder
* HTTPX
* Nuclei

## Clone

```bash
git clone <repository-url>
cd RYNEX
```

## Create virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## Install Python dependencies

```bash
pip install -r requirements.txt
```

## Configure environment

Create `.env`:

```env
DATABASE_URL=postgresql+psycopg2://USER:PASSWORD@localhost:5432/rynex
```

## Start API

```bash
uvicorn backend.app.main:app --reload
```

API:

```text
http://127.0.0.1:8000
```

Health check:

```text
GET /health
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

---

# 🔐 Authorization & Safety

RYNEX is intended to be used **only against systems for which the operator has explicit authorization**.

Do not scan:

* Third-party infrastructure
* Company/client infrastructure without authorization
* Random internet targets
* Systems outside your permitted scope

The project is designed as a defensive security research and portfolio platform.

Scanning configuration should remain appropriately conservative for the authorized environment.

---

# 🗺️ Roadmap

## Day 1 — Foundation

* [x] FastAPI
* [x] PostgreSQL
* [x] SQLAlchemy
* [x] Domain/Asset/Scan models

## Day 2 — Asset Discovery

* [x] Subfinder
* [x] DNS
* [x] IP tracking
* [x] Asset lifecycle

## Day 3 — Exposure Mapping

* [x] Nmap
* [x] Port tracking
* [x] HTTPX
* [x] Technology tracking

## Day 4 — Vulnerability Engine

* [x] Nuclei
* [x] Finding ingestion
* [x] Finding lifecycle

## Day 5 — Intelligence Layer

* [x] Contextual risk scoring
* [x] Asset risk
* [x] Asset changes
* [x] Port changes
* [x] Technology changes
* [x] Finding changes
* [x] Historical state
* [x] Full scan orchestration

## Day 6 — Security Dashboard

* [ ] Dashboard overview
* [ ] Asset inventory
* [ ] Asset detail
* [ ] Finding management
* [ ] Risk visualization
* [ ] Change timeline
* [ ] Search/filtering

## Day 7 — Production-Quality Portfolio MVP

* [ ] Automated tests
* [ ] Scanner failure handling
* [ ] Validation
* [ ] Logging cleanup
* [ ] Final database cleanup
* [ ] Architecture diagram
* [ ] Screenshots
* [ ] Complete documentation
* [ ] GitHub polish
* [ ] Resume project entry

---

# 📌 Current Limitations

As of Day 5:

* The dashboard has not yet been implemented.
* Scan execution is currently synchronous through the API.
* The platform is designed for local MVP operation.
* Scanner configuration remains intentionally conservative.
* Final failure-state hardening is planned for Day 7.
* The current risk engine is an internal prioritization model, not CVSS.
* Authentication and multi-user functionality are outside the current 7-day MVP scope.

---

# 🔮 Future Improvements

Potential future versions could include:

* Scheduled scanning
* Background job processing
* Authentication/RBAC
* Notification integrations
* Cloud deployment
* Multi-tenant architecture
* Advanced asset relationship graphs
* Historical risk trend visualization
* Additional security scanners

These are intentionally **outside the current 7-day MVP**.

---

# 📈 Development Progress

```text
Day 1  ████████████████████ 100%
Day 2  ████████████████████ 100%
Day 3  ████████████████████ 100%
Day 4  ████████████████████ 100%
Day 5  ████████████████████ 100%
Day 6  ░░░░░░░░░░░░░░░░░░░░   0%
Day 7  ░░░░░░░░░░░░░░░░░░░░   0%

Overall: ~71%
```

---

# 📄 Project Status

**RYNEX is currently at the end of Day 5 of its 7-day MVP development plan.**

The core security intelligence backend is operational:

```text
Discovery
   +
Exposure Mapping
   +
Vulnerability Detection
   +
Risk Calculation
   +
Change Detection
   +
Historical State
   =
RYNEX Core Engine
```

The next milestone is the **analyst-facing security dashboard**.

---

## ⚠️ Disclaimer

RYNEX is an educational, defensive-security, and portfolio project.

Only use it against infrastructure that you own or have explicit authorization to assess.
