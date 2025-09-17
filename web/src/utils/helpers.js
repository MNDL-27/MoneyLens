// Format file size for display
export const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 Bytes';
  
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
};

// Format currency for display
export const formatCurrency = (amount, currency = 'USD') => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: currency,
  }).format(amount);
};

// Format date for display
export const formatDate = (dateString) => {
  try {
    const date = new Date(dateString);
    return date.toLocaleString();
  } catch (error) {
    return dateString;
  }
};

// Download blob as file
export const downloadBlob = (blob, filename) => {
  const url = window.URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  window.URL.revokeObjectURL(url);
};

// Validate PDF file
export const validatePDFFile = (file) => {
  const errors = [];
  
  if (!file) {
    errors.push('No file selected');
    return errors;
  }
  
  if (file.type !== 'application/pdf') {
    errors.push('File must be a PDF');
  }
  
  const maxSize = 10 * 1024 * 1024; // 10MB
  if (file.size > maxSize) {
    errors.push(`File size must be less than ${formatFileSize(maxSize)}`);
  }
  
  return errors;
};

// Truncate text for display
export const truncateText = (text, maxLength = 100) => {
  if (text.length <= maxLength) return text;
  return text.substr(0, maxLength) + '...';
};

// Generate unique ID
export const generateId = () => {
  return Math.random().toString(36).substr(2, 9);
};