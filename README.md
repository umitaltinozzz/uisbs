# UISBS

**National Drug Stock & Information System — Turkey**

[![FastAPI](https://img.shields.io/badge/FastAPI-Python_3.11-009688?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5-3178C6?style=for-the-badge&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL+PostGIS-15-336791?style=for-the-badge&logo=postgresql&logoColor=white)](https://postgis.net/)
[![Redis](https://img.shields.io/badge/Redis-7-DC382D?style=for-the-badge&logo=redis&logoColor=white)](https://redis.io/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![License: AGPL v3](https://img.shields.io/badge/License-AGPL_v3-darkred?style=for-the-badge)](./LICENSE)
[![Status](https://img.shields.io/badge/Status-Archived-gray?style=for-the-badge)]()

---

> *This project began out of desperation — watching my father fight cancer while the medicine he needed was nowhere to be found in our city.*

## The Story

In 2024, my father was diagnosed with cancer. One of the hardest parts of his treatment wasn't the illness itself — it was the hours spent calling pharmacy after pharmacy, trying to find medications that had been prescribed but were simply **not available anywhere nearby**.

Standing in the middle of that helplessness, I kept asking myself one question:

**Why doesn't this information exist in one place?**

If a pharmacy has a drug in stock and a patient doesn't know it — that is a data problem. And data problems have software solutions.

That's why I built UISBS.

## Overview

UIBS (Ulusal İlaç Stok ve Bilgi Sistemi) is a centralized platform where pharmacies across Turkey can share their real-time drug inventory, and patients or caregivers can search for medications available near them — filtered by location using PostGIS geospatial queries.

**Data collected from public sources:**
- **90,000+** drug records — barcode, active ingredient, ATC code, manufacturer, category
- **40,000+** pharmacy records — province, district, address, phone number

Sample dataset included: [`ilce_eczaneler_20250528_001708.csv`](./ilce_eczaneler_20250528_001708.csv)

## Features

- **Location-based drug search** — PostGIS distance queries; find pharmacies with your medication nearby
- **Real-time inventory** — Pharmacies update stock; patients see live data
- **Role-based access control** — Citizen / Pharmacy / Government Official / Admin
- **Full audit logging** — Every critical action is logged for compliance
- **JWT + OAuth2 authentication** — Secure, stateless token flow
- **OpenAPI / Swagger docs** — Auto-generated at `/docs`

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI, Python 3.11, Uvicorn |
| Frontend | React 18, TypeScript, Tailwind CSS |
| Database | PostgreSQL 15 + PostGIS |
| Cache | Redis 7 |
| Auth | JWT + OAuth2, RBAC |
| Infrastructure | Docker, Docker Compose |

## Getting Started

```bash
git clone https://github.com/umitaltinozzz/uisbs.git
cd uisbs

# Copy environment config
cp backend/.env.example backend/.env

# Start infrastructure
docker-compose up -d postgres redis

# Start backend
docker-compose up -d backend

# Start frontend
cd frontend && npm install && npm start
```

| Service | URL |
|---|---|
| Frontend | http://localhost:3000 |
| Backend API | http://localhost:8000 |
| Swagger Docs | http://localhost:8000/docs |

## Project Structure

```
uisbs/
├── backend/
│   ├── app/
│   │   ├── api/v1/
│   │   │   ├── api.py
│   │   │   └── endpoints/
│   │   │       ├── auth.py          # Register, login, token refresh, logout
│   │   │       ├── drugs.py         # Drug search & detail
│   │   │       ├── pharmacies.py    # Pharmacy listing & geosearch
│   │   │       ├── search.py        # Combined location-aware search
│   │   │       ├── stocks.py        # Inventory management
│   │   │       ├── users.py         # User profile & management
│   │   │       └── admin.py         # Admin-only operations
│   │   ├── core/
│   │   │   ├── config.py            # App settings (Pydantic)
│   │   │   └── database.py          # SQLAlchemy + PostGIS engine
│   │   ├── models/
│   │   │   ├── user.py              # User model (RBAC roles)
│   │   │   ├── drug.py              # Drug & ATC models
│   │   │   ├── pharmacy.py          # Pharmacy + geolocation model
│   │   │   └── audit_log.py         # Audit trail model
│   │   ├── schemas/
│   │   │   └── user.py              # Pydantic request/response schemas
│   │   ├── services/
│   │   │   ├── auth_service.py      # Auth business logic
│   │   │   └── audit_service.py     # Audit logging service
│   │   ├── utils/
│   │   │   └── security.py          # Password hashing, JWT helpers
│   │   └── main.py                  # FastAPI app entry point
│   ├── .env.example
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   └── src/
│       ├── components/
│       │   ├── Auth/
│       │   │   └── ProtectedRoute.tsx
│       │   └── Layout/
│       │       ├── Header.tsx
│       │       ├── Footer.tsx
│       │       └── Layout.tsx
│       ├── contexts/
│       │   └── AuthContext.tsx
│       ├── pages/
│       │   ├── HomePage.tsx
│       │   ├── Auth/
│       │   │   ├── LoginPage.tsx
│       │   │   └── RegisterPage.tsx
│       │   ├── Search/
│       │   │   └── SearchPage.tsx
│       │   └── Pharmacy/
│       │       └── PharmacyDashboard.tsx
│       ├── App.tsx
│       └── index.tsx
├── ilce_eczaneler_20250528_001708.csv
├── docker-compose.yml
└── .gitignore
```

## Why It Was Left Unfinished

Scaling this system nationwide hit walls that no individual developer can climb alone:

- **Ministry of Health license** — Centralizing pharmacy stock data requires an official MoH permit
- **KVKK / GDPR compliance** — Formal DPAs and a designated DPO required
- **Pharmacists' Association (TEB) approval** — Pharmacies need professional body sign-off to join third-party platforms
- **ITS integration** — Turkey's national drug tracking system (İlaç Takip Sistemi) requires a separate, bureaucratic integration process

These are institutional problems, not technical ones. The code and data are here for anyone — a company, a ministry, a researcher — who can take it further.

## A Final Word

My father finished his treatment. I paused this project — but I haven't forgotten what those days felt like.

I hope that someday this problem is actually solved. So that no patient ever suffers because they couldn't find a drug that exists.

## License

[GNU Affero General Public License v3.0](./LICENSE) — Any use of this code, including running it as a network service, requires the full source to remain open. No one can close this and profit from it without giving back.
