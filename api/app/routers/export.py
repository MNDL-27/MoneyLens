# api/app/routers/export.py
from fastapi import APIRouter, Body
from fastapi.responses import StreamingResponse
import io
import csv
from typing import List, Dict, Any

router = APIRouter()

@router.post("/csv")
def export_csv(payload: Dict[str, Any] = Body(...)):
    transactions: List[Dict[str, Any]] = payload.get("transactions", [])
    buf = io.StringIO()
    writer = csv.DictWriter(
        buf,
        fieldnames=[
            "date",
            "description",
            "amount",
            "type",
            "balance",
            "currency",
            "source_account",
        ],
    )
    writer.writeheader()
    for t in transactions:
        writer.writerow(t)
    buf.seek(0)
    return StreamingResponse(
        iter([buf.read()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=moneylens_transactions.csv"},
    )
