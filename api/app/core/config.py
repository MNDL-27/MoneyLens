from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_debug: bool = False
    
    # File Upload Configuration  
    max_file_size: int = 10485760  # 10MB
    upload_dir: str = "/tmp/uploads"
    allowed_extensions: str = "pdf"
    
    # PDF Processing Configuration
    ocr_enabled: bool = True
    ocr_language: str = "eng"
    text_extraction_timeout: int = 30
    
    # Database Configuration
    database_url: str = "sqlite:///./moneylens.db"
    
    class Config:
        env_prefix = "ML_"
        env_file = ".env"


settings = Settings()

# Ensure upload directory exists
os.makedirs(settings.upload_dir, exist_ok=True)