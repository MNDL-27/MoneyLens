import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { validatePDFFile, formatFileSize } from '../utils/helpers';
import './FileUpload.css';

const FileUpload = ({ onUpload, isUploading }) => {
  const [uploadError, setUploadError] = useState(null);

  const onDrop = useCallback((acceptedFiles, rejectedFiles) => {
    setUploadError(null);
    
    if (rejectedFiles.length > 0) {
      const errors = rejectedFiles.map(rejection => 
        rejection.errors.map(error => error.message).join(', ')
      );
      setUploadError(errors.join('; '));
      return;
    }

    if (acceptedFiles.length > 0) {
      const file = acceptedFiles[0];
      const validationErrors = validatePDFFile(file);
      
      if (validationErrors.length > 0) {
        setUploadError(validationErrors.join('; '));
        return;
      }

      onUpload(file);
    }
  }, [onUpload]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf']
    },
    maxFiles: 1,
    maxSize: 10 * 1024 * 1024, // 10MB
    disabled: isUploading
  });

  return (
    <div className="file-upload">
      <div 
        {...getRootProps()} 
        className={`dropzone ${isDragActive ? 'active' : ''} ${isUploading ? 'disabled' : ''}`}
      >
        <input {...getInputProps()} />
        
        <div className="dropzone-content">
          <div className="upload-icon">📄</div>
          
          {isUploading ? (
            <div className="upload-status">
              <div className="spinner"></div>
              <p>Uploading...</p>
            </div>
          ) : (
            <>
              <h3>Upload PDF Document</h3>
              <p>
                {isDragActive 
                  ? 'Drop the PDF file here...' 
                  : 'Drag & drop a PDF file here, or click to select'
                }
              </p>
              <div className="upload-limits">
                <small>Max file size: {formatFileSize(10 * 1024 * 1024)}</small>
              </div>
            </>
          )}
        </div>
      </div>
      
      {uploadError && (
        <div className="error-message">
          <strong>Upload Error:</strong> {uploadError}
        </div>
      )}
    </div>
  );
};

export default FileUpload;