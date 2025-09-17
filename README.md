<<<<<<< HEAD
# MoneyLens — Run Guide

## Prerequisites
- Docker and Docker Compose installed
- Ports available: WEB_PORT (default 8080), API_PORT (default 8000)

## 1) Configure env
cd compose
cp .env.example .env
# Edit .env if needed (WEB_PORT, API_PORT, ML_* toggles)

## 2) Development (hot reload API + Vite dev server)
cd compose
docker compose -f docker-compose.dev.yml up --build
# Open http://localhost:${WEB_PORT}

## 3) Production-like (nginx static + api)
cd compose
docker compose -f docker-compose.yml up --build
# Open http://localhost:${WEB_PORT}

## 4) Rebuild after code changes
# Dev:
docker compose -f docker-compose.dev.yml build --no-cache api
# Prod:
docker compose -f docker-compose.yml build --no-cache

## 5) Common tips
# Check container logs
docker logs -f moneylens-api
docker logs -f moneylens-web

# Health endpoints
curl http://localhost:${API_PORT}/healthz

# Large PDFs
# Increase ML_MAX_UPLOAD_MB in compose/.env and restart compose.

# OCR quality
# Increase ML_OCR_DPI (e.g., 300 -> 400) if scanned text is poor.

# CORS for external hosts
# Add the web origin to ML_ALLOWED_ORIGINS in compose/.env.

## 6) Project layout (key)
api/   -> FastAPI app with text-first parsing and OCR fallback
web/   -> Vite+React SPA, proxies /api to backend in dev and prod
compose/ -> docker-compose files and env
=======
# MoneyLens
>>>>>>> 7e217e39ced6cd2cfb3984a1f29c06a7393003cc
