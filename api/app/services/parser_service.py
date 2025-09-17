# api/app/services/parser_service.py
from typing import Dict, Any, List, Optional
from app.services.text_extractor import extract_transactions_from_text
from app.services.ocr_extractor import extract_transactions_from_ocr
from app.services.totals import compute_totals, balance_check
from app.models.responses import Transaction

MIN_ROWS_FOR_SUCCESS = 5

def _enough_rows(rows: List[dict]) -> bool:
    return len(rows) >= MIN_ROWS_FOR_SUCCESS

def parse_pdf_statement(pdf_path: str, mode: str = "auto") -> Dict[str, Any]:
    """
    mode: "auto" (default), "text", or "ocr"
    Returns dict with keys: totals, transactions, metadata
    """
    metadata: Dict[str, Any] = {}
    rows: List[dict] = []

    if mode in ("auto", "text"):
        rows = extract_transactions_from_text(pdf_path)
        metadata["mode_used"] = "text"
        if mode == "auto" and not _enough_rows(rows):
            rows = []
            metadata["mode_used"] = None

    if mode == "ocr" or (mode == "auto" and not rows):
        rows = extract_transactions_from_ocr(pdf_path)
        metadata["mode_used"] = "ocr"

    transactions: List[Transaction] = [Transaction(**r) for r in rows]
    totals = compute_totals(transactions)

    # Try to use first/last known balance for a basic check
    opening: Optional[float] = next((t.balance for t in transactions if t.balance is not None), None)
    closing: Optional[float] = next((t.balance for t in reversed(transactions) if t.balance is not None), None)
    bc = balance_check(opening, closing, totals)
    if bc:
        metadata["balance_check"] = {
            "opening": bc[0],
            "closing": bc[1],
            "expected_closing": bc[2],
        }

    metadata["transaction_count"] = len(transactions)

    return {
        "totals": totals.model_dump(),
        "transactions": [t.model_dump() for t in transactions],
        "metadata": metadata,
    }
