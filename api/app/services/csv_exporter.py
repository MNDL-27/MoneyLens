import pandas as pd
import io
from typing import List, Dict, Any
from app.models.schemas import ParseResult, CSVExportRequest
from app.services.file_manager import FileManager


class CSVExporter:
    def __init__(self, file_manager: FileManager):
        self.file_manager = file_manager
    
    def export_results(self, export_request: CSVExportRequest) -> bytes:
        """Export parse results to CSV format."""
        data = []
        
        for file_id in export_request.file_ids:
            parse_result = self.file_manager.get_parse_result(file_id)
            file_info = self.file_manager.get_file_info(file_id)
            
            if not parse_result or not file_info:
                continue
            
            # Base row data
            base_row = {
                "file_id": file_id,
                "filename": parse_result.filename,
                "upload_time": file_info.get("upload_time", ""),
                "processing_time": parse_result.processing_time,
                "text_extraction_method": parse_result.parsed_text.method,
            }
            
            # Add parsed text if requested
            if export_request.include_text:
                base_row["parsed_text"] = parse_result.parsed_text.text
            
            # Add metadata if requested
            if export_request.include_metadata:
                for key, value in parse_result.metadata.items():
                    base_row[f"metadata_{key}"] = value
            
            # Create a row for each financial total found
            if parse_result.totals:
                for i, total in enumerate(parse_result.totals):
                    row = base_row.copy()
                    row.update({
                        "total_index": i + 1,
                        "total_label": total.label,
                        "total_value": total.value,
                        "total_currency": total.currency,
                        "total_line_number": total.line_number
                    })
                    data.append(row)
            else:
                # If no totals found, still include the file info
                row = base_row.copy()
                row.update({
                    "total_index": 0,
                    "total_label": "None Found",
                    "total_value": 0.0,
                    "total_currency": "USD",
                    "total_line_number": None
                })
                data.append(row)
        
        # Create DataFrame and export to CSV
        if not data:
            # Return empty CSV with headers
            headers = [
                "file_id", "filename", "upload_time", "processing_time",
                "text_extraction_method", "total_index", "total_label",
                "total_value", "total_currency", "total_line_number"
            ]
            if export_request.include_text:
                headers.append("parsed_text")
            
            df = pd.DataFrame(columns=headers)
        else:
            df = pd.DataFrame(data)
        
        # Convert to CSV bytes
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        return csv_buffer.getvalue().encode('utf-8')
    
    def export_summary(self, file_ids: List[str]) -> bytes:
        """Export a summary CSV with one row per file."""
        data = []
        
        for file_id in file_ids:
            parse_result = self.file_manager.get_parse_result(file_id)
            file_info = self.file_manager.get_file_info(file_id)
            
            if not parse_result or not file_info:
                continue
            
            # Find the highest value total
            highest_total = None
            if parse_result.totals:
                highest_total = max(parse_result.totals, key=lambda x: x.value)
            
            row = {
                "file_id": file_id,
                "filename": parse_result.filename,
                "upload_time": file_info.get("upload_time", ""),
                "processing_time": parse_result.processing_time,
                "text_extraction_method": parse_result.parsed_text.method,
                "totals_found": len(parse_result.totals),
                "highest_total_label": highest_total.label if highest_total else "None",
                "highest_total_value": highest_total.value if highest_total else 0.0,
                "highest_total_currency": highest_total.currency if highest_total else "USD",
                "all_totals": "; ".join([
                    f"{t.label}: {t.value} {t.currency}" 
                    for t in parse_result.totals
                ]) if parse_result.totals else "None found"
            }
            
            data.append(row)
        
        # Create DataFrame and export to CSV
        df = pd.DataFrame(data) if data else pd.DataFrame(columns=[
            "file_id", "filename", "upload_time", "processing_time",
            "text_extraction_method", "totals_found", "highest_total_label",
            "highest_total_value", "highest_total_currency", "all_totals"
        ])
        
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        return csv_buffer.getvalue().encode('utf-8')