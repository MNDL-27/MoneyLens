# Pydantic schemas for ParseResult and Totals
from pydantic import BaseModel
from typing import List, Dict, Any

class Totals(BaseModel):
    inflow: float
    outflow: float
    net: float

class TransactionRow(BaseModel):
    date: str
    desc: str
    amount: float

class ParseResult(BaseModel):
    totals: Dict[str, float]
    rows: List[Dict[str, Any]]
