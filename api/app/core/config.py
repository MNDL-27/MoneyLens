# api/app/core/config.py
import os
from typing import List

def _csv(name: str, default: str) -> List[str]:
    return [x.strip() for x in os.getenv(name, default).split(",") if x.strip()]

class Settings:
    allowed_origins = _csv("ML_ALLOWED_ORIGINS", "http://localhost:49155")
    max_upload_mb = int(os.getenv("ML_MAX_UPLOAD_MB", "20"))
    ocr_enabled = os.getenv("ML_OCR_ENABLED", "true").lower() == "true"
    ocr_dpi = int(os.getenv("ML_OCR_DPI", "300"))

settings = Settings()
