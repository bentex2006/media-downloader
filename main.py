"""
FastAPI backend for Multi-Platform Media Downloader
This is the main server file that handles all API endpoints
Created by: Ritu Raj Singh
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel
import os
import uvicorn
import logging
from downloader import MediaDownloader
from config import AppConfig

# Configure logging to help with debugging
# This will show us what's happening during downloads
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
# This creates our web server that will handle all requests
app = FastAPI(
    title="Multi-Platform Media Downloader",
    description="Download videos, music, and images from social media platforms",
    version="1.0.0"
)

# Mount static files directory
# This serves our HTML, CSS, and JavaScript files to users
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/downloads", StaticFiles(directory="downloads"), name="downloads")

# Initialize our media downloader
# This is the core component that handles yt-dlp operations
downloader = MediaDownloader()

# Pydantic models for request validation
# These define the structure of data we expect from frontend
class DownloadRequest(BaseModel):
    url: str  # The media URL user wants to download
    format: str  # MP4, MP3, or IMAGE
    quality: str = "best"  # Video quality preference

class DownloadResponse(BaseModel):
    success: bool
    message: str
    download_url: str = None
    filename: str = None

# Root endpoint - serves our main HTML page
@app.get("/", response_class=HTMLResponse)
async def root():
    """
    Serves the main application page
    This is what users see when they visit our site
    """
    try:
        with open("static/index.html", "r") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Frontend not found")

# Health check endpoint
@app.get("/health")
async def health_check():
    """
    Simple health check to ensure server is running
    Useful for monitoring and debugging
    """
    return {"status": "healthy", "message": "Media downloader is running"}

# Main download endpoint
@app.post("/api/download", response_model=DownloadResponse)
async def download_media(request: DownloadRequest):
    """
    Handles media download requests from frontend
    This is where the magic happens - we take a URL and return a downloaded file
    
    Args:
        request: Contains URL, format, and quality preferences
    
    Returns:
        DownloadResponse with success status and file information
    """
    try:
        logger.info(f"Download request received: {request.url}, format: {request.format}")
        
        # Validate the URL format
        # Basic check to ensure we have a valid URL
        if not request.url or not request.url.startswith(('http://', 'https://')):
            return DownloadResponse(
                success=False,
                message="Please provide a valid URL starting with http:// or https://"
            )
        
        # Validate format selection
        # Ensure user selected a supported format
        valid_formats = ['MP4', 'MP3', 'IMAGE']
        if request.format.upper() not in valid_formats:
            return DownloadResponse(
                success=False,
                message=f"Invalid format. Please choose from: {', '.join(valid_formats)}"
            )
        
        # Attempt to download the media
        # This calls our downloader service to handle the actual download
        result = await downloader.download_media(
            url=request.url,
            format=request.format.upper(),
            quality=request.quality
        )
        
        if result["success"]:
            # If download succeeded, return file information
            return DownloadResponse(
                success=True,
                message="Download completed successfully!",
                download_url=f"/downloads/{result['filename']}",
                filename=result['filename']
            )
        else:
            # If download failed, return error message
            return DownloadResponse(
                success=False,
                message=result["error"]
            )
            
    except Exception as e:
        # Handle any unexpected errors
        logger.error(f"Download error: {str(e)}")
        return DownloadResponse(
            success=False,
            message=f"An error occurred during download: {str(e)}"
        )

# Get list of supported platforms
@app.get("/api/platforms")
async def get_supported_platforms():
    """
    Returns list of supported platforms for frontend display
    Helps users know which sites they can download from
    """
    return {
        "platforms": [
            "YouTube",
            "Instagram", 
            "Twitter/X",
            "Pinterest",
            "TikTok",
            "Facebook",
            "And many more via yt-dlp"
        ]
    }

# Clean up old files endpoint
@app.post("/api/cleanup")
async def cleanup_downloads():
    """
    Removes old downloaded files to save disk space
    This prevents our server from filling up with old downloads
    """
    try:
        downloads_dir = "downloads"
        if os.path.exists(downloads_dir):
            files_removed = 0
            for filename in os.listdir(downloads_dir):
                if filename != ".gitkeep":  # Keep our directory placeholder
                    file_path = os.path.join(downloads_dir, filename)
                    os.remove(file_path)
                    files_removed += 1
            
            return {
                "success": True,
                "message": f"Cleaned up {files_removed} files"
            }
        return {
            "success": True,
            "message": "Downloads directory is already clean"
        }
    except Exception as e:
        logger.error(f"Cleanup error: {str(e)}")
        return {
            "success": False,
            "message": f"Cleanup failed: {str(e)}"
        }

# Run the server when this file is executed directly
if __name__ == "__main__":
    # Create downloads directory if it doesn't exist
    # This ensures we have a place to store downloaded files
    os.makedirs("downloads", exist_ok=True)
    
    print("🚀 Starting Multi-Platform Media Downloader")
    print("📱 Frontend will be available at: http://localhost:5000")
    print("🔧 API documentation at: http://localhost:5000/docs")
    print("👨‍💻 Created by: Ritu Raj Singh")
    
    # Start the server with uvicorn
    # Host 0.0.0.0 makes it accessible from outside the container
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=5000,
        reload=True,  # Auto-reload on code changes during development
        log_level="info"
    )
