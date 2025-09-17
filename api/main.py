from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
import logging

from app.api.endpoints import router
from app.core.config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Create FastAPI app
app = FastAPI(
    title="MoneyLens API",
    description="PDF processing API for financial document analysis",
    version="1.0.0",
    debug=settings.api_debug
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api")

@app.get("/")
async def root():
    """Root endpoint - redirect to docs."""
    return RedirectResponse(url="/docs")

@app.get("/api")
async def api_root():
    """API root endpoint."""
    return {
        "name": "MoneyLens API",
        "version": "1.0.0",
        "description": "PDF processing API for financial document analysis",
        "endpoints": {
            "upload": "/api/upload",
            "process": "/api/process/{file_id}",
            "result": "/api/result/{file_id}",
            "files": "/api/files",
            "export": "/api/export/csv",
            "summary": "/api/export/csv/summary",
            "health": "/api/health"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.api_debug
    )