import React, { useState } from 'react';
import { formatCurrency, formatDate, truncateText, downloadBlob } from '../utils/helpers';
import { apiService } from '../services/api';
import './ResultsDisplay.css';

const ResultsDisplay = ({ results, onDelete, onExport }) => {
  const [selectedFiles, setSelectedFiles] = useState(new Set());
  const [exportOptions, setExportOptions] = useState({
    includeText: false,
    includeMetadata: false
  });
  const [isExporting, setIsExporting] = useState(false);

  const handleFileSelect = (fileId) => {
    const newSelected = new Set(selectedFiles);
    if (newSelected.has(fileId)) {
      newSelected.delete(fileId);
    } else {
      newSelected.add(fileId);
    }
    setSelectedFiles(newSelected);
  };

  const handleSelectAll = () => {
    if (selectedFiles.size === results.length) {
      setSelectedFiles(new Set());
    } else {
      setSelectedFiles(new Set(results.map(r => r.file_id)));
    }
  };

  const handleExportSelected = async () => {
    if (selectedFiles.size === 0) return;

    setIsExporting(true);
    try {
      const blob = await apiService.exportCSV(Array.from(selectedFiles), exportOptions);
      downloadBlob(blob, `moneylens_export_${new Date().toISOString().split('T')[0]}.csv`);
    } catch (error) {
      console.error('Export failed:', error);
      alert('Export failed. Please try again.');
    } finally {
      setIsExporting(false);
    }
  };

  const handleExportSummary = async () => {
    setIsExporting(true);
    try {
      const blob = await apiService.exportSummaryCSV();
      downloadBlob(blob, `moneylens_summary_${new Date().toISOString().split('T')[0]}.csv`);
    } catch (error) {
      console.error('Summary export failed:', error);
      alert('Summary export failed. Please try again.');
    } finally {
      setIsExporting(false);
    }
  };

  if (!results || results.length === 0) {
    return (
      <div className="results-display">
        <div className="empty-state">
          <h3>No processed files yet</h3>
          <p>Upload and process PDF files to see results here.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="results-display">
      <div className="results-header">
        <h2>Processing Results</h2>
        
        <div className="bulk-actions">
          <button 
            onClick={handleSelectAll}
            className="btn btn-secondary"
          >
            {selectedFiles.size === results.length ? 'Deselect All' : 'Select All'}
          </button>
          
          <button 
            onClick={handleExportSelected}
            disabled={selectedFiles.size === 0 || isExporting}
            className="btn btn-primary"
          >
            {isExporting ? 'Exporting...' : `Export Selected (${selectedFiles.size})`}
          </button>
          
          <button 
            onClick={handleExportSummary}
            disabled={isExporting}
            className="btn btn-success"
          >
            Export Summary
          </button>
        </div>
      </div>

      <div className="export-options">
        <label>
          <input
            type="checkbox"
            checked={exportOptions.includeText}
            onChange={(e) => setExportOptions(prev => ({
              ...prev,
              includeText: e.target.checked
            }))}
          />
          Include extracted text
        </label>
        
        <label>
          <input
            type="checkbox"
            checked={exportOptions.includeMetadata}
            onChange={(e) => setExportOptions(prev => ({
              ...prev,
              includeMetadata: e.target.checked
            }))}
          />
          Include metadata
        </label>
      </div>

      <div className="results-grid">
        {results.map((result) => (
          <div key={result.file_id} className="result-card">
            <div className="card-header">
              <div className="file-selection">
                <input
                  type="checkbox"
                  checked={selectedFiles.has(result.file_id)}
                  onChange={() => handleFileSelect(result.file_id)}
                />
              </div>
              
              <div className="file-info">
                <h3 title={result.filename}>{truncateText(result.filename, 30)}</h3>
                <p className="file-meta">
                  Processed: {formatDate(result.upload_time)} | 
                  Method: {result.parsed_text?.method || 'N/A'} |
                  Time: {result.processing_time?.toFixed(2)}s
                </p>
              </div>
              
              <button 
                onClick={() => onDelete(result.file_id)}
                className="delete-btn"
                title="Delete file"
              >
                🗑️
              </button>
            </div>

            <div className="card-content">
              <div className="totals-section">
                <h4>Financial Totals Found ({result.totals?.length || 0})</h4>
                
                {result.totals && result.totals.length > 0 ? (
                  <div className="totals-list">
                    {result.totals.map((total, index) => (
                      <div key={index} className="total-item">
                        <span className="total-label">{total.label}:</span>
                        <span className="total-value">
                          {formatCurrency(total.value, total.currency)}
                        </span>
                        {total.line_number && (
                          <span className="total-line">
                            (Line {total.line_number})
                          </span>
                        )}
                      </div>
                    ))}
                  </div>
                ) : (
                  <p className="no-totals">No financial totals detected</p>
                )}
              </div>

              <div className="text-preview">
                <h4>Text Preview</h4>
                <div className="text-content">
                  {result.parsed_text?.text ? 
                    truncateText(result.parsed_text.text, 200) : 
                    'No text extracted'
                  }
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ResultsDisplay;