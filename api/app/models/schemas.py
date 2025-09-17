from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime


class UploadResponse(BaseModel):
    file_id: str
    filename: str
    size: int
    upload_time: datetime


class ParsedText(BaseModel):
    text: str
    method: str  # "text" or "ocr"
    confidence: Optional[float] = None


class FinancialTotal(BaseModel):
    label: str
    value: float
    currency: str = "USD"
    line_number: Optional[int] = None


class ParseResult(BaseModel):
    file_id: str
    filename: str
    parsed_text: ParsedText
    totals: List[FinancialTotal]
    processing_time: float
    metadata: Dict[str, Any]


class CSVExportRequest(BaseModel):
    file_ids: List[str]
    include_text: bool = False
    include_metadata: bool = False


class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
    code: Optional[str] = None