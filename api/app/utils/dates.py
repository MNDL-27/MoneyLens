# api/app/utils/dates.py
from datetime import datetime

DATE_FORMATS = [
    "%d/%m/%Y",
    "%d-%m-%Y",
    "%d %b %Y",
    "%d %B %Y",
    "%Y-%m-%d",
    "%m/%d/%Y",
]

def parse_date(s: str) -> str:
    """
    Try multiple formats and return ISO date (YYYY-MM-DD) on success.
    If parsing fails, return the original string unchanged.
    """
    if s is None:
        return ""
    s = s.strip()
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(s, fmt).date().isoformat()
        except Exception:
            continue
    return s
