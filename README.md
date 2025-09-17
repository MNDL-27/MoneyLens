# MoneyLens

**PDF Financial Document Analysis Tool**

MoneyLens is a comprehensive web application for processing financial PDF documents. It extracts text content and automatically identifies financial totals using a combination of direct text extraction and OCR (Optical Character Recognition) fallback. The application provides a modern web interface for uploading documents, viewing results, and exporting data to CSV format.

## Features

### 📄 PDF Processing
- **Text-first extraction** using pdfplumber for optimal accuracy
- **OCR fallback** with pytesseract when text extraction yields minimal results
- **Financial totals detection** using intelligent regex patterns
- **Support for various financial document types** (invoices, receipts, statements, etc.)

### 🌐 Web Interface
- **Drag & drop file upload** with validation
- **Real-time processing status** updates
- **Interactive results display** with financial totals highlighting
- **Bulk operations** for multiple files
- **Responsive design** for desktop and mobile

### 📊 Export Capabilities
- **CSV export** with customizable options
- **Summary reports** for quick overview
- **Detailed exports** including extracted text and metadata
- **Bulk export** for multiple files

### 🚀 Modern Architecture
- **FastAPI backend** with automatic documentation
- **React frontend** with Vite for fast development
- **Docker containerization** for easy deployment
- **Nginx reverse proxy** for production-ready setup
- **Environment-driven configuration** with ML_* variables

## Quick Start

### Prerequisites
- Docker and Docker Compose
- At least 2GB RAM for OCR processing
- Modern web browser

### Development Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd MoneyLens
   ```

2. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your preferred settings
   ```

3. **Start the development environment:**
   ```bash
   docker-compose up --build
   ```

4. **Access the application:**
   - Web interface: http://localhost
   - API documentation: http://localhost/api/docs
   - API direct access: http://localhost:8000
   - Web app direct: http://localhost:3000

### Production Deployment

1. **Prepare environment:**
   ```bash
   cp .env.example .env
   # Configure production settings in .env
   ```

2. **Deploy with production overrides:**
   ```bash
   docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build
   ```

## Architecture

### Services

#### API Service (`/api`)
- **Framework:** FastAPI with uvicorn
- **Dependencies:** pdfplumber, pytesseract, pandas
- **Features:**
  - PDF upload and validation
  - Text extraction with OCR fallback
  - Financial totals detection
  - CSV export generation
  - File management and cleanup

#### Web Service (`/web`)
- **Framework:** React with Vite
- **Features:**
  - File upload interface
  - Results visualization
  - Export controls
  - Responsive design

#### Nginx Service (`/nginx`)
- **Purpose:** Reverse proxy and static file serving
- **Configuration:**
  - Routes `/api/*` to API service
  - Routes `/*` to web application
  - Handles large file uploads
  - Gzip compression
  - Security headers

### Data Flow

1. **Upload:** User uploads PDF through web interface
2. **Processing:** API extracts text and identifies financial totals
3. **Storage:** Results stored with file metadata
4. **Display:** Web interface shows processed results
5. **Export:** Users can export data to CSV format

## Configuration

All configuration is handled through environment variables with the `ML_` prefix:

### API Configuration
- `ML_API_HOST`: API server host (default: 0.0.0.0)
- `ML_API_PORT`: API server port (default: 8000)
- `ML_API_DEBUG`: Enable debug mode (default: false)

### File Processing
- `ML_MAX_FILE_SIZE`: Maximum upload size in bytes (default: 10MB)
- `ML_UPLOAD_DIR`: Upload directory path (default: /tmp/uploads)
- `ML_ALLOWED_EXTENSIONS`: Allowed file extensions (default: pdf)

### OCR Configuration
- `ML_OCR_ENABLED`: Enable OCR fallback (default: true)
- `ML_OCR_LANGUAGE`: OCR language (default: eng)
- `ML_TEXT_EXTRACTION_TIMEOUT`: Processing timeout (default: 30s)

### Infrastructure
- `ML_NGINX_PORT`: Nginx port (default: 80)
- `ML_WEB_PORT`: Web development server port (default: 3000)

## API Documentation

The FastAPI backend provides interactive documentation at `/api/docs` when running. Key endpoints include:

- `POST /api/upload` - Upload PDF file
- `POST /api/process/{file_id}` - Process uploaded file
- `GET /api/result/{file_id}` - Get processing result
- `GET /api/files` - List all processed files
- `POST /api/export/csv` - Export selected files to CSV
- `GET /api/export/csv/summary` - Export summary CSV
- `DELETE /api/file/{file_id}` - Delete file and results

## Development

### Backend Development
```bash
cd api
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Development
```bash
cd web
npm install
npm run dev
```

### Testing

The application includes comprehensive error handling and validation. For manual testing:

1. Upload various PDF types (text-based and image-based)
2. Verify financial totals detection accuracy
3. Test CSV export functionality
4. Check file cleanup and deletion

## Troubleshooting

### Common Issues

**OCR not working:**
- Ensure tesseract is installed in the container
- Check ML_OCR_ENABLED setting
- Verify PDF contains readable content

**Upload failures:**
- Check file size against ML_MAX_FILE_SIZE
- Ensure file is valid PDF format
- Verify upload directory permissions

**Processing timeouts:**
- Increase ML_TEXT_EXTRACTION_TIMEOUT
- Check available system resources
- Consider file complexity

### Logs

View service logs:
```bash
docker-compose logs api
docker-compose logs web
docker-compose logs nginx
```

## License

This project is licensed under the GNU Affero General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review API documentation at `/api/docs`
3. Create an issue in the repository