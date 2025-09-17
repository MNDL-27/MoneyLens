# api/app/routers/health.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/healthz")
def healthz():
    return {"status": "ok"}

@router.get("/version")
def version():
    return {"name": "MoneyLens API", "version": "0.1.0"}
