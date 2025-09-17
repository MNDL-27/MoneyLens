# MoneyLens

> **Parse bank statement PDFs with a FastAPI backend (text-first, OCR fallback) and a Vite+React SPA frontend.**
> **Run locally or in production with Docker Compose.**
# MoneyLens

> **Run locally or in production with Docker Compose.**

## Features
- **Text-first parsing** with [pdfplumber](https://github.com/jsvine/pdfplumber); **OCR fallback** via [pdf2image](https://github.com/Belval/pdf2image) + [Tesseract](https://github.com/tesseract-ocr/tesseract) for scanned PDFs.
- **Endpoints:**
	- `GET /healthz` — health check
	- `GET /version` — API version
	- `POST /parse/pdf` — upload and parse statement
	- `POST /export/csv` — export last parse as CSV
- **Web app:**
	- Upload PDF, choose mode (auto | text | ocr)
	- View totals & transactions
	- Export CSV
- **Dockerized:**
	- Dev (hot reload) and prod-like (Nginx static + API) Compose setups

## Prerequisites
- Docker & Docker Compose installed
- Default ports: `WEB_PORT=8080`, `API_PORT=8000` (configurable)

## Quick start (production‑like)
```
cd compose
cp .env.example .env
# Optionally edit WEB_PORT, API_PORT, ML_* values in .env
docker compose -f docker-compose.yml up --build
```
Open [http://localhost:8080](http://localhost:8080) (or your chosen `WEB_PORT`).

## Development (hot reload)
Runs Vite dev server for the web and a reloadable FastAPI API. [memory:8]
```
cd compose
docker compose -f docker-compose.dev.yml up --build
```
Open [http://localhost:8080](http://localhost:8080). In dev, `/api` is proxied by Vite to the API container.

## Environment variables (ML_*)
These are read by the API via pydantic‑settings (env prefix ML_). Set them in `compose/.env`. [memory:9]
- `ML_MAX_UPLOAD_MB` — Maximum upload size in MB (default: 20)
- `ML_OCR_ENABLED` — Enable OCR fallback (`true`/`false`, default: true)
- `ML_OCR_DPI` — Rasterization DPI for OCR (e.g., 300 or 400)
- `ML_ALLOWED_ORIGINS` — Comma-separated list for CORS (e.g., `http://localhost:8080`)

## Useful commands
Check logs:
```
docker logs -f moneylens-api
docker logs -f moneylens-web
```
Health check:
```
curl http://localhost:8000/healthz
```
Rebuild images:
```
# Dev: rebuild API only
docker compose -f compose/docker-compose.dev.yml build --no-cache api

# Prod-like: rebuild everything
docker compose -f compose/docker-compose.yml build --no-cache
```
---

## Project layout
```
api/       FastAPI service, text + OCR extraction, totals, CSV export
web/       Vite + React SPA, Nginx for prod build, dev proxy to /api
compose/   Docker Compose files and .env template
```
---

## Local tooling (optional)
If running the API without Docker, ensure system packages are installed:
If running the API without Docker, ensure system packages are installed:
- Poppler (for pdf2image)
- Tesseract OCR
- Python 3.11+

Then:
```sh
cd api
uvicorn app.main:app --reload --port 8000
```

And run the web dev server:
```sh
cd web
npm install
npm run dev
```
Open [http://localhost:8080](http://localhost:8080).

## License
---

## 📄 License

MIT
```

If a “Screenshots” or “Roadmap” section is needed later, it can be appended with images and planned tasks.
