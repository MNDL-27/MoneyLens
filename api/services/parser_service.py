# Orchestrates text-first parsing then OCR fallback

def parse_bank_statement(file_path: str):
    # TODO: implement text and OCR pipeline
    return {"totals": {"inflow": 1000, "outflow": 500, "net": 500}, "rows": [{"date": "2025-01-01", "desc": "Mock", "amount": 1000}]}
