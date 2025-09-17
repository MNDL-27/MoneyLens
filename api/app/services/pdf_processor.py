import pdfplumber
import pytesseract
from PIL import Image
import io
import re
import logging
from typing import List, Tuple, Optional
from app.models.schemas import ParsedText, FinancialTotal
from app.core.config import settings

logger = logging.getLogger(__name__)


class PDFProcessor:
    def __init__(self):
        self.ocr_enabled = settings.ocr_enabled
        self.ocr_language = settings.ocr_language
        
    def extract_text(self, pdf_path: str) -> ParsedText:
        """Extract text from PDF, with OCR fallback if needed."""
        try:
            # Try text extraction first
            text = self._extract_text_directly(pdf_path)
            if text and len(text.strip()) > 20:  # Minimum text threshold
                return ParsedText(text=text, method="text")
            
            # Fallback to OCR if text extraction fails or produces little text
            if self.ocr_enabled:
                logger.info(f"Text extraction yielded minimal results, falling back to OCR for {pdf_path}")
                ocr_text = self._extract_text_with_ocr(pdf_path)
                return ParsedText(text=ocr_text, method="ocr")
            else:
                return ParsedText(text=text or "", method="text")
                
        except Exception as e:
            logger.error(f"Error extracting text from {pdf_path}: {str(e)}")
            raise
    
    def _extract_text_directly(self, pdf_path: str) -> str:
        """Extract text directly from PDF using pdfplumber."""
        text_content = []
        
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    text_content.append(text)
        
        return "\n".join(text_content)
    
    def _extract_text_with_ocr(self, pdf_path: str) -> str:
        """Extract text using OCR as fallback."""
        text_content = []
        
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages):
                try:
                    # Convert page to image
                    img = page.to_image(resolution=300)
                    pil_img = img.original
                    
                    # Apply OCR
                    ocr_text = pytesseract.image_to_string(
                        pil_img, 
                        lang=self.ocr_language,
                        config='--psm 6'  # Assume a single uniform block of text
                    )
                    
                    if ocr_text.strip():
                        text_content.append(ocr_text)
                        
                except Exception as e:
                    logger.warning(f"OCR failed for page {page_num + 1}: {str(e)}")
                    continue
        
        return "\n".join(text_content)
    
    def extract_financial_totals(self, text: str) -> List[FinancialTotal]:
        """Extract financial totals from text using regex patterns."""
        totals = []
        
        # Common patterns for financial amounts
        patterns = [
            # Total: $123.45, Total $123.45, Total: 123.45
            (r'(?i)total[\s:]*\$?([0-9,]+\.?[0-9]*)', 'Total'),
            # Subtotal: $123.45
            (r'(?i)subtotal[\s:]*\$?([0-9,]+\.?[0-9]*)', 'Subtotal'),
            # Tax: $123.45
            (r'(?i)tax[\s:]*\$?([0-9,]+\.?[0-9]*)', 'Tax'),
            # Amount Due: $123.45, Amount: $123.45
            (r'(?i)amount[\s\w]*[\s:]*\$?([0-9,]+\.?[0-9]*)', 'Amount'),
            # Balance: $123.45, Balance Due: $123.45
            (r'(?i)balance[\s\w]*[\s:]*\$?([0-9,]+\.?[0-9]*)', 'Balance'),
            # Grand Total: $123.45
            (r'(?i)grand[\s]+total[\s:]*\$?([0-9,]+\.?[0-9]*)', 'Grand Total'),
        ]
        
        lines = text.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            for pattern, label in patterns:
                matches = re.finditer(pattern, line)
                for match in matches:
                    try:
                        # Clean and convert the amount
                        amount_str = match.group(1).replace(',', '')
                        amount = float(amount_str)
                        
                        # Skip very small amounts (likely false positives)
                        if amount >= 0.01:
                            totals.append(FinancialTotal(
                                label=label,
                                value=amount,
                                currency="USD",
                                line_number=line_num
                            ))
                    except (ValueError, IndexError):
                        continue
        
        # Remove duplicates and sort by value (descending)
        unique_totals = []
        seen_values = set()
        
        for total in sorted(totals, key=lambda x: x.value, reverse=True):
            if total.value not in seen_values:
                unique_totals.append(total)
                seen_values.add(total.value)
        
        return unique_totals[:10]  # Limit to top 10 results