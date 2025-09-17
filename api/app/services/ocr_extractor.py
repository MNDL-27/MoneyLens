# api/app/services/ocr_extractor.py
from typing import List, Dict
from pdf2image import convert_from_path
import pytesseract
import re
from app.utils.numbers import parse_amount
from app.utils.dates import parse_date
from app.core.config import settings

def extract_transactions_from_ocr(pdf_path: str) -> List[Dict]:
    """
    Convert PDF pages to images (DPI from settings), OCR with Tesseract,
    and parse lines by splitting on runs of spaces, assuming the last token is the amount.
    """
    rows: List[Dict] = []
    images = convert_from_path(pdf_path, dpi=settings.ocr_dpi)
    for img in images:
        # OCR; could add config like --oem 1 --psm 6 if needed
        text = pytesseract.image_to_string(img)
        for raw in text.splitlines():
            line = raw.strip()
            if not line:
                continue
            # Split by gaps; aim to capture: Date | Description ... | Amount
            parts = re.split(r"\s{2,}", line)
            if len(parts) < 2:
                continue
            last = parts[-1]
            amt = parse_amount(last)
            # Skip lines that don't end with numeric-looking amount
            if amt == 0.0 and not re.search(r"\d", last):
                continue
            # Date may be first token, but not always; try parse
            date = parse_date(parts[0])
            desc = " ".join(parts[1:-1]).strip() if len(parts) > 2 else (parts[0] if date == parts[0] else parts[1])
            rows.append({
                "date": date,
                "description": desc,
                "amount": amt,
                "type": "credit" if amt > 0 else "debit",
                "balance": None
            })
    return rows
