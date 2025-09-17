# api/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.routers import parse, health, export

app = FastAPI(title="MoneyLens API", version="0.1.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(health.router, prefix="")
app.include_router(parse.router, prefix="/parse", tags=["parse"])
app.include_router(export.router, prefix="/export", tags=["export"])
