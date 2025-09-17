# api/app/core/config.py
import os
from typing import List

def _csv_env(name: str, default: str) -> List[str]:
    return [x.strip() for x in os.getenv(name, default).split(",") if x.strip()]

class Settings:
    allowed_origins: List[str]
    max_upload_mb: int
    ocr_enabled: bool
    ocr_dpi: int

    def __init__(self) -> None:
        self.allowed_origins = _csv_env("ML_ALLOWED_ORIGINS", "http://localhost:49155")
        self.max_upload_mb = int(os.getenv("ML_MAX_UPLOAD_MB", "20"))
        self.ocr_enabled = os.getenv("ML_OCR_ENABLED", "true").lower() == "true"
        self.ocr_dpi = int(os.getenv("ML_OCR_DPI", "300"))

settings = Settings()
