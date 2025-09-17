# api/Dockerfile
FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# System deps for OCR + PDF
RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    poppler-utils \
    libjpeg62-turbo \
    zlib1g \
    libtiff6 \
    libpng16-16 \
    fonts-dejavu-core \
    wget ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Dependencies via pyproject or requirements
COPY pyproject.toml /app/
RUN pip install --no-cache-dir --upgrade pip setuptools wheel \
 && pip install --no-cache-dir .

# Copy source
COPY app /app/app

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
