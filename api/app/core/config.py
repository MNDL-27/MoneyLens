# api/app/core/config.py
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    max_upload_mb: int = 20
    ocr_enabled: bool = True
    ocr_dpi: int = 300
    allowed_origins: List[str] = ["http://localhost:8080", "http://127.0.0.1:8080"]

    class Config:
        env_prefix = "ML_"
        env_file = ".env"

settings = Settings()
