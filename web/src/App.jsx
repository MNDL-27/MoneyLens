import React, { useState, useEffect } from 'react';
import FileUpload from './components/FileUpload';
import ResultsDisplay from './components/ResultsDisplay';
import { apiService } from './services/api';
import './App.css';

function App() {
  const [results, setResults] = useState([]);
  const [isUploading, setIsUploading] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [error, setError] = useState(null);
  const [status, setStatus] = useState('Ready to upload files');

  // Load existing results on component mount
  useEffect(() => {
    loadResults();
  }, []);

  const loadResults = async () => {
    try {
      const response = await apiService.listFiles();
      const files = response.files || [];
      
      // Get detailed results for each file
      const detailedResults = await Promise.all(
        files.map(async (file) => {
          try {
            const result = await apiService.getResult(file.file_id);
            return result;
          } catch (error) {
            console.error(`Failed to load result for ${file.file_id}:`, error);
            return null;
          }
        })
      );
      
      setResults(detailedResults.filter(result => result !== null));
    } catch (error) {
      console.error('Failed to load results:', error);
      setError('Failed to load existing results');
    }
  };

  const handleFileUpload = async (file) => {
    setIsUploading(true);
    setError(null);
    setStatus('Uploading file...');

    try {
      // Upload file
      const uploadResponse = await apiService.uploadFile(file);
      setStatus('File uploaded successfully. Processing...');
      
      setIsUploading(false);
      setIsProcessing(true);

      // Process file
      const processingResult = await apiService.processFile(uploadResponse.file_id);
      
      // Add to results
      setResults(prev => [processingResult, ...prev]);
      setStatus('File processed successfully');
      
      // Clear status after delay
      setTimeout(() => setStatus('Ready to upload files'), 3000);
      
    } catch (error) {
      console.error('Upload/processing failed:', error);
      setError(error.response?.data?.detail || 'Upload or processing failed');
      setStatus('Ready to upload files');
    } finally {
      setIsUploading(false);
      setIsProcessing(false);
    }
  };

  const handleDeleteFile = async (fileId) => {
    if (!window.confirm('Are you sure you want to delete this file?')) {
      return;
    }

    try {
      await apiService.deleteFile(fileId);
      setResults(prev => prev.filter(result => result.file_id !== fileId));
      setStatus('File deleted successfully');
      setTimeout(() => setStatus('Ready to upload files'), 2000);
    } catch (error) {
      console.error('Delete failed:', error);
      setError(error.response?.data?.detail || 'Failed to delete file');
    }
  };

  const clearError = () => {
    setError(null);
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>💰 MoneyLens</h1>
        <p>PDF Financial Document Analysis</p>
      </header>

      <main className="app-main">
        <div className="status-bar">
          <div className={`status ${isProcessing ? 'processing' : ''}`}>
            {isProcessing && <div className="spinner-small"></div>}
            <span>{status}</span>
          </div>
        </div>

        {error && (
          <div className="error-banner">
            <div className="error-content">
              <strong>Error:</strong> {error}
              <button onClick={clearError} className="error-close">×</button>
            </div>
          </div>
        )}

        <section className="upload-section">
          <FileUpload 
            onUpload={handleFileUpload} 
            isUploading={isUploading || isProcessing} 
          />
        </section>

        <section className="results-section">
          <ResultsDisplay 
            results={results}
            onDelete={handleDeleteFile}
            onExport={loadResults} // Refresh after export
          />
        </section>
      </main>

      <footer className="app-footer">
        <p>
          MoneyLens - Extract financial totals from PDF documents with text analysis and OCR
        </p>
      </footer>
    </div>
  );
}

export default App;