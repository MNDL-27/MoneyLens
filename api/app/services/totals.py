# api/app/services/totals.py
from typing import List, Optional, Tuple
from app.models.responses import Transaction, Totals

def compute_totals(transactions: List[Transaction]) -> Totals:
    inflow = sum(t.amount for t in transactions if t.amount > 0)
    outflow = sum(-t.amount for t in transactions if t.amount < 0)
    net = inflow - outflow
    flow_volume = inflow + outflow
    return Totals(
        inflow=round(inflow, 2),
        outflow=round(outflow, 2),
        net=round(net, 2),
        flow_volume=round(flow_volume, 2),
    )

def balance_check(
    opening: Optional[float], closing: Optional[float], totals: Totals
) -> Optional[Tuple[float, float, float]]:
    """
    If opening and closing balances are available, compute the expected
    closing as opening + net, and return a tuple for diagnostics.
    """
    if opening is None or closing is None:
        return None
    expected = round(opening + totals.net, 2)
    return (opening, closing, expected)
