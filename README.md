<div align="center">

# 🔍 JobAggregator

### A production-grade backend system for aggregating job listings across multiple portals

<br/>

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.x-000000?style=for-the-badge&logo=flask&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup4-Scraping-43B02A?style=for-the-badge)
![REST API](https://img.shields.io/badge/REST-API-FF6C37?style=for-the-badge&logo=postman&logoColor=white)

<br/>

![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)
![PRs Welcome](https://img.shields.io/badge/PRs-Welcome-blue?style=flat-square)

</div>

---

## 📌 Overview

**JobAggregator** is a backend service that scrapes job listings from multiple portals, normalizes extracted data into a unified schema, and exposes a clean REST API for querying aggregated opportunities — all without hitting a single portal twice.

Built with a layered architecture: API → Executor → Scraper → Persistence. Each layer is independently testable and swappable.

> **Why this exists:** Job seekers waste time searching the same role across 4–5 different platforms with inconsistent UX. This solves that by centralizing the data backend.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🌐 **Multi-Portal Scraping** | Pluggable scrapers for Internshala, TimesJobs, BigShyft |
| ⚙️ **Background Execution** | Thread-based async executor — API never blocks on scrape |
| 📊 **Job Status Tracking** | In-memory store with `pending → running → completed/failed` states |
| 🔎 **Filterable Query API** | Filter by skill, location, source; paginated responses |
| 🏗️ **Modular Architecture** | Add a new portal by dropping in one scraper file |
| 🗄️ **Normalized Storage** | All portals → unified MySQL schema |

---

## 🏛️ Architecture

```
Client (HTTP)
     │
     ▼
┌─────────────────────┐
│     API Layer       │  Flask Blueprints (api/jobs, api/scrape, api/stats, api/health)
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│  Execution Layer    │  services/executors/ (base.py + thread_executor.py)
│  + Status Store     │  services/status_store.py  ←  in-memory job registry
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│   Scraper Layer     │  scrapers/ — one module per portal
│  (Internshala,      │  Each: fetch → parse → filter → normalize
│   TimesJobs, etc.)  │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│  Persistence Layer  │  extensions/db.py + models/job.py
│  MySQL via Flask-   │  Normalized schema, query service
│  SQLAlchemy         │
└─────────────────────┘
```

---

## 📁 Project Structure

```
JOB_AGGREGATOR/
│
├── app/
│   ├── api/                        # Flask Blueprints
│   │   ├── health/                 # GET /health
│   │   ├── jobs/                   # GET /jobs
│   │   ├── scrape/                 # POST /scrape
│   │   └── stats/                  # GET /stats
│   │
│   ├── config/                     # Environment configs
│   │   ├── base.py
│   │   └── development.py
│   │
│   ├── extensions/
│   │   └── db.py                   # SQLAlchemy + MySQL setup
│   │
│   ├── models/
│   │   └── job.py                  # ORM model for job listings
│   │
│   ├── scrapers/                   # One module per job portal
│   │   └── __init__.py
│   │
│   ├── services/
│   │   ├── executors/
│   │   │   ├── base.py             # Abstract executor interface
│   │   │   └── thread_executor.py  # ThreadPoolExecutor impl
│   │   ├── scraper_runner.py       # Orchestrates scraper dispatch
│   │   └── status_store.py        # In-memory job state registry
│   │
│   └── utils/
│       └── middleware.py           # Request logging, error handling
│
├── config/
├── .env
├── requirements.txt
└── run.py
```

---

## 🚀 Quickstart

### Prerequisites

- Python 3.10+
- MySQL 8.0+
- pip

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/job-aggregator.git
cd job-aggregator
```

### 2. Set up a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment

```bash
cp .env.example .env
```

Edit `.env`:

```env
FLASK_ENV=development
DB_HOST=localhost
DB_PORT=3306
DB_NAME=job_aggregator
DB_USER=root
DB_PASSWORD=yourpassword
```

### 5. Set up the database

```bash
mysql -u root -p -e "CREATE DATABASE job_aggregator;"
flask db upgrade       # or run schema.sql if migrations aren't set up
```

### 6. Run the server

```bash
python run.py
```

Server starts at `http://localhost:5000`

---

## 📡 API Reference

### `GET /health`

Check service status.

```json
{ "status": "ok", "uptime": "12m 33s" }
```

---

### `POST /scrape`

Trigger a background scraping job for a portal.

**Request:**
```json
{ "source": "internshala" }
```

**Response:**
```json
{ "job_id": "7f9a2b11", "status": "pending" }
```

Supported sources: `internshala`, `timesjobs`, `bigshyft`

---

### `GET /scrape/status/{job_id}`

Poll the execution state of a scrape job.

```json
{
  "job_id": "7f9a2b11",
  "status": "completed",
  "records_saved": 47
}
```

States: `pending` → `running` → `completed` | `failed`

---

### `GET /jobs`

Query aggregated job listings.

**Query params:**

| Param | Type | Description |
|---|---|---|
| `skill` | string | Filter by skill keyword (e.g. `python`) |
| `location` | string | Filter by city (e.g. `bangalore`) |
| `source` | string | Filter by portal |
| `page` | int | Page number (default: 1) |
| `limit` | int | Results per page (default: 20) |

**Example:**
```
GET /jobs?skill=python&location=bangalore&page=1&limit=20
```

**Response:**
```json
{
  "jobs": [ { "id": 1, "title": "Backend Engineer", "company": "Razorpay", ... } ],
  "page": 1,
  "limit": 20,
  "total": 148
}
```

---

### `GET /stats`

Aggregated counts by source, skill frequency, location distribution.

---

## 🗄️ Database Schema

```sql
CREATE TABLE jobs (
  id          INT AUTO_INCREMENT PRIMARY KEY,
  title       VARCHAR(255),
  company     VARCHAR(255),
  skills      TEXT,
  experience  VARCHAR(100),
  salary      VARCHAR(100),
  location    VARCHAR(100),
  source      VARCHAR(50),
  created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

---

## ⚙️ How Scraping Works

Each scraper in `app/scrapers/` follows the same interface:

```
1. Fetch paginated HTML from the job portal
2. Parse with BeautifulSoup
3. Extract: title, company, skills, experience, salary, location
4. Normalize field names to match the unified schema
5. Write to MySQL via the Job model
```

Scrapers are dispatched by `scraper_runner.py`, which calls `thread_executor.py` to run them in a background thread. The `status_store.py` tracks state in memory — no DB writes needed for job tracking overhead.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.10+ |
| Web Framework | Flask |
| Scraping | BeautifulSoup4 + Requests |
| Database | MySQL + Flask-SQLAlchemy |
| Async Execution | ThreadPoolExecutor |
| Config Management | python-dotenv |

---

## 🧩 Adding a New Portal

1. Create `app/scrapers/newportal.py`
2. Implement the scraper following the existing interface:
   ```python
   def scrape(keyword: str) -> list[dict]:
       # fetch, parse, normalize
       return jobs
   ```
3. Register it in `app/scrapers/__init__.py`
4. That's it — the executor and API pick it up automatically

---



<div align="center">
  <sub>Built with Python, Flask, and too many job portals. ☕</sub>
</div>
