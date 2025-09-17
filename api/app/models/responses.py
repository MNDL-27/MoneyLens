# api/app/models/responses.py
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class Transaction(BaseModel):
    date: str
    description: str
    amount: float
    type: str  # "credit" or "debit"
    balance: Optional[float] = None
    currency: Optional[str] = None
    source_account: Optional[str] = None

class Totals(BaseModel):
    inflow: float
    outflow: float
    net: float
    flow_volume: float

class ParseResult(BaseModel):
    totals: Totals
    transactions: List[Transaction]
    metadata: Dict[str, Any]
