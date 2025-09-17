import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || '/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000, // 30 seconds for file processing
});

export const apiService = {
  // Upload PDF file
  uploadFile: async (file) => {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await api.post('/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  // Process uploaded file
  processFile: async (fileId) => {
    const response = await api.post(`/process/${fileId}`);
    return response.data;
  },

  // Get processing result
  getResult: async (fileId) => {
    const response = await api.get(`/result/${fileId}`);
    return response.data;
  },

  // List all processed files
  listFiles: async () => {
    const response = await api.get('/files');
    return response.data;
  },

  // Export results to CSV
  exportCSV: async (fileIds, options = {}) => {
    const response = await api.post('/export/csv', {
      file_ids: fileIds,
      include_text: options.includeText || false,
      include_metadata: options.includeMetadata || false,
    }, {
      responseType: 'blob',
    });
    return response.data;
  },

  // Export summary CSV
  exportSummaryCSV: async () => {
    const response = await api.get('/export/csv/summary', {
      responseType: 'blob',
    });
    return response.data;
  },

  // Delete file
  deleteFile: async (fileId) => {
    const response = await api.delete(`/file/${fileId}`);
    return response.data;
  },

  // Health check
  healthCheck: async () => {
    const response = await api.get('/health');
    return response.data;
  },
};

export default apiService;