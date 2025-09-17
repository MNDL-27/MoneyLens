# api/app/services/text_extractor.py
from typing import List, Dict
import pdfplumber
import re
from app.utils.numbers import parse_amount
from app.utils.dates import parse_date

def extract_transactions_from_text(pdf_path: str) -> List[Dict]:
    """
    Try to extract rows from tables first; if no tables are found,
    parse lines by splitting on runs of spaces, assuming right-aligned amounts.
    """
    rows: List[Dict] = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            if tables:
                for tbl in tables:
                    for raw in tbl:
                        cols = [c.strip() if isinstance(c, str) else "" for c in raw]
                        if len(cols) < 3:
                            continue
                        date = parse_date(cols[0])
                        # Find numeric-looking columns
                        num_idx = [i for i, c in enumerate(cols) if re.search(r"[0-9]", c or "")]
                        amount = None
                        balance = None
                        if num_idx:
                            amount = parse_amount(cols[num_idx[-1]])
                            if len(num_idx) > 1:
                                balance = parse_amount(cols[num_idx[-2]])
                        desc_parts = []
                        # Use middle columns for description if present
                        for i in range(1, max(1, len(cols) - 2)):
                            if i not in num_idx:
                                desc_parts.append(cols[i])
                        desc = " ".join(p for p in desc_parts if p).strip() or (cols[1] if len(cols) > 1 else "")
                        if amount is None:
                            continue
                        rows.append({
                            "date": date,
                            "description": desc,
                            "amount": amount,
                            "type": "credit" if amount > 0 else "debit",
                            "balance": balance
                        })
            else:
                # Fallback: line-based parsing
                text = page.extract_text() or ""
                for line in text.splitlines():
                    line = line.strip()
                    if not line:
                        continue
                    parts = re.split(r"\s{2,}", line)
                    if len(parts) < 3:
                        continue
                    date = parse_date(parts[0])
                    last = parts[-1]
                    amt = parse_amount(last)
                    if amt == 0.0 and not re.search(r"\d", last):
                        continue
                    desc = " ".join(parts[1:-1]).strip()
                    rows.append({
                        "date": date,
                        "description": desc,
                        "amount": amt,
                        "type": "credit" if amt > 0 else "debit",
                        "balance": None
                    })
    return rows
