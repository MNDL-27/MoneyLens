# api/app/routers/parse.py
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from tempfile import NamedTemporaryFile
import shutil
from app.core.config import settings
from app.services.parser_service import parse_pdf_statement

router = APIRouter()

@router.post("/pdf")
async def parse_pdf(
    file: UploadFile = File(...),
    mode: str = Form("auto"),  # auto | text | ocr
):
    # Basic content-type check
    if file.content_type not in ("application/pdf", "application/octet-stream"):
        raise HTTPException(status_code=400, detail="Invalid file type (expecting PDF)")

    # Size guard if the client provided size header (not always available)
    size = getattr(file, "size", None)
    if size is not None and size > settings.max_upload_mb * 1024 * 1024:
        raise HTTPException(status_code=413, detail="File too large")

    # Persist to a temp file for parser backends
    with NamedTemporaryFile(delete=True, suffix=".pdf") as tmp:
        with open(tmp.name, "wb") as out:
            shutil.copyfileobj(file.file, out)
        try:
            result = parse_pdf_statement(tmp.name, mode=mode)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Parse error: {e}")

    return JSONResponse(result)
