# api/app/utils/numbers.py
import re

CURRENCY_CHARS = "₹$€£¥₨৳₽﷼₩₺₫"

def parse_amount(s: str) -> float:
    """
    Convert a string like '₹ 1,23,456.78' or '(1,234.56)' to float.
    Removes currency symbols, spaces, and thousands separators.
    Supports Indian and Western grouping; treats parentheses as negative.
    """
    if s is None:
        return 0.0
    s = str(s).strip().replace("\u00a0", " ")
    negative = False

    # Parentheses for negatives: (123.45)
    if s.startswith("(") and s.endswith(")"):
        negative = True
        s = s[1:-1]

    # Remove currency symbols and common non-numeric chars except sign and dot/comma
    s = re.sub(fr"[{re.escape(CURRENCY_CHARS)}\s]", "", s)

    # If both comma and dot exist, assume comma is thousands sep, dot is decimal
    if "," in s and "." in s:
        s = s.replace(",", "")
    # If only comma exists, assume comma is thousands or decimal; prefer thousands
    elif "," in s and "." not in s:
        # If there are multiple commas, drop them all
        s = s.replace(",", "")

    # Keep digits, sign, and single dot
    s = re.sub(r"[^0-9\.\-\+]", "", s)

    if s in ("", "-", "+", ".", "-.", "+."):
        return 0.0

    try:
        val = float(s)
    except ValueError:
        return 0.0

    return -val if negative else val
