# POST /parse/pdf endpoint stub
from fastapi import APIRouter, UploadFile, File
from api.models.responses import ParseResult

router = APIRouter()

@router.post("/parse/pdf", response_model=ParseResult)
def parse_pdf(file: UploadFile = File(...)):
    # TODO: parse PDF and return results
    return ParseResult(totals={"inflow": 1000, "outflow": 500, "net": 500}, rows=[{"date": "2025-01-01", "desc": "Mock", "amount": 1000}])
