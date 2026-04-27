<br>
<p align="center">
  <img src="https://img.shields.io/badge/Status-Archived-red?style=for-the-badge" alt="Status"/>
  <img src="https://img.shields.io/github/license/aikirbaclayan/Ulusal-ilac-stok-takip-sistemi-uisbs?style=for-the-badge&color=darkred&label=License" alt="License"/>
  <img src="https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/FastAPI-0.104-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI"/>
  <img src="https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react&logoColor=black" alt="React"/>
  <img src="https://img.shields.io/badge/TypeScript-5-3178C6?style=for-the-badge&logo=typescript&logoColor=white" alt="TypeScript"/>
  <img src="https://img.shields.io/badge/PostgreSQL+PostGIS-15-336791?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL"/>
  <img src="https://img.shields.io/badge/Redis-7-DC382D?style=for-the-badge&logo=redis&logoColor=white" alt="Redis"/>
  <img src="https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker"/>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Drug%20Records-90%2C000%2B-orange?style=flat-square" alt="Drug Records"/>
  <img src="https://img.shields.io/badge/Pharmacy%20Records-40%2C000%2B-green?style=flat-square" alt="Pharmacy Records"/>
  <img src="https://img.shields.io/badge/Coverage-Turkey%20Nationwide-red?style=flat-square&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAzMiAxNiI+PC9zdmc+" alt="Coverage"/>
  <img src="https://img.shields.io/badge/Made%20with-%E2%9D%A4%EF%B8%8F%20in%20Turkey-red?style=flat-square" alt="Made with love"/>
</p>

---

# UISBS — National Drug Stock & Information System

> *This project began out of desperation — watching my father fight cancer while the medicine he needed was nowhere to be found in our city.*

---

## The Story Behind This Project

In 2024, my father was diagnosed with cancer. One of the hardest parts of his treatment wasn't the illness itself — it was the hours spent calling pharmacy after pharmacy, trying to find medications that had been prescribed but were simply **not available anywhere nearby**.

Standing in the middle of that helplessness, I kept asking myself one question:

**Why doesn't this information exist in one place?**

If a pharmacy has a drug in stock and a patient doesn't know it — that is a data problem. And data problems have software solutions.

That's why I built UISBS.

---

## What Is UISBS?

**UISBS (Ulusal İlaç Stok ve Bilgi Sistemi — National Drug Stock & Information System)** is a centralized platform where pharmacies across Turkey can share their real-time drug inventory, and patients or caregivers can search for medications available near them.

### Data Collected

All data was compiled from publicly available sources:

| Dataset | Records | Content |
|---------|---------|---------|
| Drug Database | **90,000+** | Barcode, active ingredient, category, manufacturer, ATC code |
| Pharmacy Database | **40,000+** | Province, district, address, phone number |

Sample data file: [`ilce_eczaneler_20250528_001708.csv`](./ilce_eczaneler_20250528_001708.csv)

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Python 3.11 / FastAPI / Uvicorn |
| Frontend | TypeScript / React 18 / Tailwind CSS |
| Database | PostgreSQL 15 + PostGIS (geospatial queries) |
| Auth | JWT + OAuth2 / Role-based access control |
| Cache | Redis 7 |
| Infrastructure | Docker / Docker Compose |
| API Docs | OpenAPI / Swagger (auto-generated) |

### Features

- **Location-based drug search** — Find pharmacies with your medication nearby using PostGIS distance calculations
- **Real-time inventory management** — Pharmacies update their stock; patients see live data
- **Role-based access control** — Separate permissions for citizens, pharmacies, government officials, and admins
- **Full audit logging** — Every critical action is logged for compliance and security
- **Geospatial indexing** — Optimized for large-scale geographic queries across all of Turkey
- **KVKK / GDPR-aware architecture** — Data handling designed with privacy regulations in mind

---

## Why It Was Left Unfinished

I set out to scale this system nationwide — and eventually across EU member states. What I encountered were regulatory walls that no individual developer can climb alone:

| Barrier | Details |
|---------|---------|
| **Ministry of Health License** | Operating a platform that centralizes pharmacy stock data in Turkey requires an official license from the Ministry of Health |
| **KVKK / GDPR Compliance** | Processing patient and pharmacy data demands formal Data Processing Agreements and a designated DPO |
| **Pharmacists' Association Approval** | Pharmacies cannot join third-party platforms without formal approval from their professional association (TEB) |
| **ITS Integration** | Any drug tracking platform must integrate with Turkey's existing İlaç Takip Sistemi (ITS), which is an entirely separate bureaucratic process |

These are not technical problems. They are institutional problems — the kind that require a company, a government partnership, or both.

I paused the project because I'm one developer. But the problem is real. The code and data are here for anyone who can take it further.

---

## Getting Started

```bash
# Clone the repository
git clone https://github.com/aikirbaclayan/Ulusal-ilac-stok-takip-sistemi-uisbs.git
cd Ulusal-ilac-stok-takip-sistemi-uisbs

# Start infrastructure (PostgreSQL + PostGIS + Redis)
docker-compose up -d postgres redis

# Start the backend API
docker-compose up -d backend

# Start the frontend (development server)
cd frontend
npm install
npm start
```

**Service URLs:**

| Service | URL |
|---------|-----|
| Frontend | http://localhost:3000 |
| Backend API | http://localhost:8000 |
| API Documentation (Swagger) | http://localhost:8000/docs |
| API Documentation (ReDoc) | http://localhost:8000/redoc |

---

## Project Structure

```
UISBS/
├── backend/
│   ├── app/
│   │   ├── api/v1/endpoints/   # REST API endpoints
│   │   ├── core/               # Config & database
│   │   ├── models/             # SQLAlchemy ORM models
│   │   ├── schemas/            # Pydantic validation schemas
│   │   ├── services/           # Business logic
│   │   └── utils/              # Security & helpers
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   └── src/
│       ├── components/         # Reusable UI components
│       ├── pages/              # Route-level page components
│       └── contexts/           # React context (auth, etc.)
├── ilce_eczaneler_20250528_001708.csv   # Pharmacy dataset
├── docker-compose.yml
└── README.md
```

---

## Contributing / Contact

This project is **not actively maintained**. However:

- If you're a researcher or developer working on a similar problem,
- If you have connections to a health ministry or public institution,
- If you want to discuss the regulatory landscape,
- Or if you simply want to continue where I left off —

Feel free to open an issue or reach out directly. I'm happy to share the full datasets and technical context with anyone who can take this further.

---

## A Final Word

My father finished his treatment. I paused this project — but I haven't forgotten what those days felt like.

I hope that someday — through public initiative or private effort — this problem is actually solved. So that no patient ever has to suffer because they couldn't find a drug that exists.

---

## License

This project is licensed under the **GNU Affero General Public License v3.0 (AGPL-3.0)**.

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg?style=for-the-badge)](https://www.gnu.org/licenses/agpl-3.0)

**What this means:**

- **You can** use, study, modify, and distribute this software freely
- **You must** release your source code if you distribute modified versions
- **You must** release your source code even if you run this as a network service (SaaS) — this is the key difference from GPL
- **You cannot** take this code, close it, and sell it as a proprietary product without contributing back

This license was chosen to ensure that any organization — commercial or governmental — that builds upon this work must contribute their improvements back to the public. The data here represents a real public health problem. It should remain in the public interest.

See the [`LICENSE`](./LICENSE) file for the full legal text.
