import os
import uuid
import shutil
import json
from typing import Dict, List, Optional
from datetime import datetime
from app.core.config import settings
from app.models.schemas import ParseResult


class FileManager:
    def __init__(self):
        self.upload_dir = settings.upload_dir
        self.metadata_file = os.path.join(self.upload_dir, "metadata.json")
        self._ensure_directories()
        self._load_metadata()
    
    def _ensure_directories(self):
        """Ensure upload and metadata directories exist."""
        os.makedirs(self.upload_dir, exist_ok=True)
    
    def _load_metadata(self):
        """Load metadata from file."""
        if os.path.exists(self.metadata_file):
            try:
                with open(self.metadata_file, 'r') as f:
                    self.metadata = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.metadata = {}
        else:
            self.metadata = {}
    
    def _save_metadata(self):
        """Save metadata to file."""
        try:
            with open(self.metadata_file, 'w') as f:
                json.dump(self.metadata, f, indent=2, default=str)
        except IOError as e:
            raise Exception(f"Failed to save metadata: {str(e)}")
    
    def save_uploaded_file(self, file_content: bytes, original_filename: str) -> str:
        """Save uploaded file and return file ID."""
        file_id = str(uuid.uuid4())
        file_extension = os.path.splitext(original_filename)[1].lower()
        stored_filename = f"{file_id}{file_extension}"
        file_path = os.path.join(self.upload_dir, stored_filename)
        
        try:
            with open(file_path, 'wb') as f:
                f.write(file_content)
            
            # Store metadata
            self.metadata[file_id] = {
                "original_filename": original_filename,
                "stored_filename": stored_filename,
                "file_path": file_path,
                "upload_time": datetime.utcnow().isoformat(),
                "size": len(file_content),
                "processed": False
            }
            self._save_metadata()
            
            return file_id
            
        except IOError as e:
            raise Exception(f"Failed to save file: {str(e)}")
    
    def get_file_path(self, file_id: str) -> Optional[str]:
        """Get file path for a given file ID."""
        if file_id in self.metadata:
            return self.metadata[file_id]["file_path"]
        return None
    
    def get_file_info(self, file_id: str) -> Optional[Dict]:
        """Get file information for a given file ID."""
        return self.metadata.get(file_id)
    
    def save_parse_result(self, file_id: str, parse_result: ParseResult):
        """Save parse result for a file."""
        if file_id in self.metadata:
            self.metadata[file_id]["processed"] = True
            self.metadata[file_id]["parse_result"] = parse_result.model_dump()
            self._save_metadata()
    
    def get_parse_result(self, file_id: str) -> Optional[ParseResult]:
        """Get parse result for a file."""
        if file_id in self.metadata and "parse_result" in self.metadata[file_id]:
            result_data = self.metadata[file_id]["parse_result"]
            return ParseResult(**result_data)
        return None
    
    def get_all_processed_files(self) -> List[str]:
        """Get list of all processed file IDs."""
        return [
            file_id for file_id, info in self.metadata.items() 
            if info.get("processed", False)
        ]
    
    def delete_file(self, file_id: str) -> bool:
        """Delete a file and its metadata."""
        if file_id not in self.metadata:
            return False
        
        file_info = self.metadata[file_id]
        file_path = file_info["file_path"]
        
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
            
            del self.metadata[file_id]
            self._save_metadata()
            return True
            
        except (OSError, IOError):
            return False
    
    def cleanup_old_files(self, max_age_days: int = 7):
        """Clean up files older than specified days."""
        cutoff_date = datetime.utcnow().timestamp() - (max_age_days * 24 * 60 * 60)
        
        files_to_delete = []
        for file_id, info in self.metadata.items():
            upload_time = datetime.fromisoformat(info["upload_time"]).timestamp()
            if upload_time < cutoff_date:
                files_to_delete.append(file_id)
        
        for file_id in files_to_delete:
            self.delete_file(file_id)