"""
FastAPI backend for Multi-Platform Media Downloader
This is the main server file that handles all API endpoints
Created by: Ritu Raj Singh
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse, StreamingResponse
from pydantic import BaseModel
import os
import uvicorn
import logging
import asyncio
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
# Note: We'll handle downloads manually to auto-delete files

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
    download_url: str = ""
    filename: str = ""

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
            format_type=request.format.upper(),
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

# Get media info for preview (without downloading)
@app.post("/api/media-info")
async def get_media_info(request: DownloadRequest):
    """
    Extract media information for preview without downloading
    This helps show users what they're about to download
    """
    try:
        logger.info(f"Media info request: {request.url}")
        
        # Validate URL
        if not request.url or not request.url.startswith(('http://', 'https://')):
            raise HTTPException(status_code=400, detail="Invalid URL")
        
        # Get media information using downloader
        info = await downloader.get_media_info(request.url)
        
        if info["success"]:
            return {
                "success": True,
                "title": info.get("title", "Unknown Title"),
                "duration": info.get("duration", "Unknown"),
                "thumbnail": info.get("thumbnail", None),
                "platform": info.get("platform", "Unknown Platform"),
                "filesize": info.get("filesize", "Unknown Size")
            }
        else:
            return {"success": False, "error": info["error"]}
            
    except Exception as e:
        logger.error(f"Media info error: {str(e)}")
        return {"success": False, "error": str(e)}

# Stream download endpoint (no file persistence)
@app.post("/api/stream-download")
async def stream_download(request: DownloadRequest):
    """
    Stream media download directly to user without saving to server
    This ensures no data persistence and faster delivery
    """
    try:
        logger.info(f"Stream download request: {request.url}")
        
        # Validate inputs
        if not request.url or not request.url.startswith(('http://', 'https://')):
            raise HTTPException(status_code=400, detail="Invalid URL")
        
        # Get the downloaded file stream
        result = await downloader.stream_download_media(
            url=request.url,
            format_type=request.format.upper(),
            quality=request.quality
        )
        
        if result["success"]:
            # Return streaming response
            return StreamingResponse(
                result["stream"],
                media_type=result["content_type"],
                headers={"Content-Disposition": f"attachment; filename={result['filename']}"}
            )
        else:
            raise HTTPException(status_code=400, detail=result["error"])
            
    except Exception as e:
        logger.error(f"Stream download error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Custom download endpoint with auto-delete
@app.get("/downloads/{filename}")
async def download_file(filename: str, background_tasks: BackgroundTasks):
    """
    Serve downloaded files and automatically delete them after delivery
    This ensures no data persistence on the server
    """
    try:
        filepath = os.path.join(AppConfig.DOWNLOADS_DIR, filename)
        
        # Check if file exists
        if not os.path.exists(filepath):
            raise HTTPException(status_code=404, detail="File not found")
        
        # Get file size for proper headers
        file_size = os.path.getsize(filepath)
        
        # Determine content type based on file extension
        content_type = "application/octet-stream"
        if filename.lower().endswith('.mp4'):
            content_type = "video/mp4"
        elif filename.lower().endswith('.mp3'):
            content_type = "audio/mpeg"
        elif filename.lower().endswith(('.jpg', '.jpeg')):
            content_type = "image/jpeg"
        elif filename.lower().endswith('.png'):
            content_type = "image/png"
        elif filename.lower().endswith('.webp'):
            content_type = "image/webp"
        
        # Schedule file deletion after response is sent
        background_tasks.add_task(delete_file_after_download, filepath)
        
        logger.info(f"Serving file: {filename} ({file_size} bytes) - will auto-delete")
        
        # Return file with proper headers
        return FileResponse(
            path=filepath,
            media_type=content_type,
            filename=filename,
            headers={
                "Content-Length": str(file_size),
                "Cache-Control": "no-cache, no-store, must-revalidate",
                "Pragma": "no-cache",
                "Expires": "0"
            }
        )
        
    except Exception as e:
        logger.error(f"Error serving file {filename}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to serve file")

def delete_file_after_download(filepath: str):
    """
    Background task to delete file after successful download
    This ensures no data persistence on the server
    """
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
            logger.info(f"✅ Auto-deleted file: {filepath}")
        else:
            logger.warning(f"File already deleted: {filepath}")
    except Exception as e:
        logger.error(f"Failed to delete file {filepath}: {str(e)}")

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

def cleanup_old_files():
    """
    Clean up any old files that might have been missed
    This runs on server startup to ensure clean state
    """
    try:
        downloads_dir = "downloads"
        if os.path.exists(downloads_dir):
            files_cleaned = 0
            for filename in os.listdir(downloads_dir):
                if filename != ".gitkeep":  # Keep our directory placeholder
                    file_path = os.path.join(downloads_dir, filename)
                    try:
                        os.remove(file_path)
                        files_cleaned += 1
                    except Exception as e:
                        logger.error(f"Failed to clean up {file_path}: {e}")
            
            if files_cleaned > 0:
                logger.info(f"🧹 Cleaned up {files_cleaned} old files on startup")
    except Exception as e:
        logger.error(f"Startup cleanup failed: {e}")

# Run the server when this file is executed directly
if __name__ == "__main__":
    # Create downloads directory if it doesn't exist
    # This ensures we have a place to store downloaded files
    os.makedirs("downloads", exist_ok=True)
    
    # Clean up any old files from previous runs
    cleanup_old_files()
    
    print("🚀 Starting Multi-Platform Media Downloader")
    print("📱 Frontend will be available at: http://localhost:5000")
    print("🔧 API documentation at: http://localhost:5000/docs")
    print("👨‍💻 Created by: Ritu Raj Singh")
    print("🗑️ Auto-delete: Files are automatically removed after download")
    
    # Start the server with uvicorn
    # Host 0.0.0.0 makes it accessible from outside the container
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=5000,
        reload=True,  # Auto-reload on code changes during development
        log_level="info"
    )
