# Settings for upload limits, OCR DPI, toggles
from pydantic import BaseSettings

class Settings(BaseSettings):
    max_upload_mb: int = 20
    ocr_enabled: bool = True
    ocr_dpi: int = 300
    allowed_origins: str = "http://localhost:8080"

settings = Settings()
