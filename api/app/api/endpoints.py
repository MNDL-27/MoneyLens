from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import StreamingResponse
from typing import List
import time
import logging
from datetime import datetime
import io

from app.models.schemas import (
    UploadResponse, ParseResult, CSVExportRequest, 
    ErrorResponse, FinancialTotal
)
from app.services.pdf_processor import PDFProcessor
from app.services.file_manager import FileManager
from app.services.csv_exporter import CSVExporter
from app.core.config import settings

logger = logging.getLogger(__name__)

router = APIRouter()

# Initialize services
file_manager = FileManager()
pdf_processor = PDFProcessor()
csv_exporter = CSVExporter(file_manager)


@router.post("/upload", response_model=UploadResponse)
async def upload_pdf(file: UploadFile = File(...)):
    """Upload a PDF file for processing."""
    
    # Validate file type
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )
    
    # Validate file size
    content = await file.read()
    if len(content) > settings.max_file_size:
        raise HTTPException(
            status_code=413,
            detail=f"File size exceeds maximum limit of {settings.max_file_size} bytes"
        )
    
    try:
        # Save the uploaded file
        file_id = file_manager.save_uploaded_file(content, file.filename)
        
        return UploadResponse(
            file_id=file_id,
            filename=file.filename,
            size=len(content),
            upload_time=datetime.utcnow()
        )
        
    except Exception as e:
        logger.error(f"Error uploading file {file.filename}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to upload file: {str(e)}"
        )


@router.post("/process/{file_id}", response_model=ParseResult)
async def process_pdf(file_id: str):
    """Process an uploaded PDF file to extract text and financial totals."""
    
    # Get file path
    file_path = file_manager.get_file_path(file_id)
    if not file_path:
        raise HTTPException(
            status_code=404,
            detail="File not found"
        )
    
    file_info = file_manager.get_file_info(file_id)
    if not file_info:
        raise HTTPException(
            status_code=404,
            detail="File information not found"
        )
    
    try:
        start_time = time.time()
        
        # Extract text from PDF
        parsed_text = pdf_processor.extract_text(file_path)
        
        # Extract financial totals
        totals = pdf_processor.extract_financial_totals(parsed_text.text)
        
        processing_time = time.time() - start_time
        
        # Create parse result
        parse_result = ParseResult(
            file_id=file_id,
            filename=file_info["original_filename"],
            parsed_text=parsed_text,
            totals=totals,
            processing_time=processing_time,
            metadata={
                "file_size": file_info["size"],
                "upload_time": file_info["upload_time"],
                "text_length": len(parsed_text.text),
                "totals_count": len(totals)
            }
        )
        
        # Save the result
        file_manager.save_parse_result(file_id, parse_result)
        
        return parse_result
        
    except Exception as e:
        logger.error(f"Error processing file {file_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process file: {str(e)}"
        )


@router.get("/result/{file_id}", response_model=ParseResult)
async def get_parse_result(file_id: str):
    """Get the parse result for a processed file."""
    
    parse_result = file_manager.get_parse_result(file_id)
    if not parse_result:
        raise HTTPException(
            status_code=404,
            detail="Parse result not found. File may not have been processed yet."
        )
    
    return parse_result


@router.get("/files")
async def list_processed_files():
    """List all processed files."""
    
    processed_files = file_manager.get_all_processed_files()
    results = []
    
    for file_id in processed_files:
        file_info = file_manager.get_file_info(file_id)
        parse_result = file_manager.get_parse_result(file_id)
        
        if file_info and parse_result:
            results.append({
                "file_id": file_id,
                "filename": file_info["original_filename"],
                "upload_time": file_info["upload_time"],
                "processing_time": parse_result.processing_time,
                "totals_count": len(parse_result.totals),
                "text_extraction_method": parse_result.parsed_text.method
            })
    
    return {"files": results}


@router.post("/export/csv")
async def export_csv(export_request: CSVExportRequest):
    """Export parse results to CSV format."""
    
    try:
        csv_data = csv_exporter.export_results(export_request)
        
        # Create filename with timestamp
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        filename = f"moneylens_export_{timestamp}.csv"
        
        return StreamingResponse(
            io.BytesIO(csv_data),
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
        
    except Exception as e:
        logger.error(f"Error exporting CSV: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to export CSV: {str(e)}"
        )


@router.get("/export/csv/summary")
async def export_summary_csv():
    """Export a summary CSV of all processed files."""
    
    try:
        processed_files = file_manager.get_all_processed_files()
        csv_data = csv_exporter.export_summary(processed_files)
        
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        filename = f"moneylens_summary_{timestamp}.csv"
        
        return StreamingResponse(
            io.BytesIO(csv_data),
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
        
    except Exception as e:
        logger.error(f"Error exporting summary CSV: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to export summary CSV: {str(e)}"
        )


@router.delete("/file/{file_id}")
async def delete_file(file_id: str):
    """Delete a file and its associated data."""
    
    success = file_manager.delete_file(file_id)
    if not success:
        raise HTTPException(
            status_code=404,
            detail="File not found"
        )
    
    return {"message": "File deleted successfully"}


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }