"""
Configuration settings for Media Downloader
This file contains all the settings and constants used throughout the app
Created by: Ritu Raj Singh
"""

import os
from typing import Dict, List

class AppConfig:
    """
    Central configuration class for the application
    This makes it easy to manage all settings in one place
    """
    
    # Basic app information
    APP_NAME = "Multi-Platform Media Downloader"
    VERSION = "1.0.0"
    CREATOR = "Ritu Raj Singh"
    
    # Creator links and information
    GITHUB_URL = "https://github.com/riturajsingh"
    LINKTREE_URL = "https://linktr.ee/riturajsingh"
    SOURCE_REPO = "https://github.com/riturajsingh/media-downloader"
    
    # Server configuration
    HOST = "0.0.0.0"  # Bind to all interfaces for container compatibility
    PORT = 5000       # Frontend port (automatically forwarded)
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"
    
    # File handling settings
    DOWNLOADS_DIR = "downloads"
    MAX_FILE_SIZE = 500 * 1024 * 1024  # 500MB limit
    
    # Supported formats and their configurations
    SUPPORTED_FORMATS = {
        "MP4": {
            "description": "Video file",
            "extensions": [".mp4"],
            "quality_options": ["best", "worst", "720p", "480p", "360p"]
        },
        "MP3": {
            "description": "Audio file", 
            "extensions": [".mp3"],
            "quality_options": ["best", "worst", "320k", "256k", "192k", "128k"]
        },
        "IMAGE": {
            "description": "Image file",
            "extensions": [".jpg", ".png", ".webp"],
            "quality_options": ["best", "original"]
        }
    }
    
    # yt-dlp configuration options
    # These are the settings we'll pass to yt-dlp for downloading
    YT_DLP_OPTIONS = {
        "outtmpl": f"{DOWNLOADS_DIR}/%(title)s.%(ext)s",  # Where to save files
        "format": "best",  # Default quality
        "noplaylist": True,  # Only download single video, not entire playlist
        "extract_flat": False,  # Get full video info
        "writesubtitles": False,  # Don't download subtitles by default
        "writeautomaticsub": False,  # Don't download auto-generated subtitles
        "ignoreerrors": True,  # Continue on errors when possible
    }
    
    # Platform-specific settings
    # Different platforms might need different handling
    PLATFORM_CONFIGS = {
        "youtube": {
            "name": "YouTube",
            "formats": ["MP4", "MP3"],
            "max_duration": 3600  # 1 hour limit
        },
        "instagram": {
            "name": "Instagram", 
            "formats": ["MP4", "IMAGE"],
            "max_duration": 600  # 10 minutes
        },
        "twitter": {
            "name": "Twitter/X",
            "formats": ["MP4", "IMAGE"],
            "max_duration": 300  # 5 minutes
        },
        "pinterest": {
            "name": "Pinterest",
            "formats": ["IMAGE"],
            "max_duration": None
        }
    }
    
    # Error messages for better user experience
    ERROR_MESSAGES = {
        "invalid_url": "Please provide a valid URL",
        "unsupported_platform": "This platform is not currently supported",
        "download_failed": "Failed to download media. Please check the URL and try again",
        "file_too_large": f"File size exceeds the {MAX_FILE_SIZE // (1024*1024)}MB limit",
        "network_error": "Network error occurred. Please check your internet connection",
        "format_not_available": "The requested format is not available for this media"
    }
    
    # Frontend configuration
    # These settings affect the user interface
    UI_CONFIG = {
        "theme": "dark",
        "primary_color": "#3b82f6",  # Blue
        "secondary_color": "#8b5cf6",  # Purple
        "success_color": "#10b981",  # Green
        "error_color": "#ef4444",    # Red
        "warning_color": "#f59e0b",  # Amber
    }
    
    @classmethod
    def get_download_path(cls, filename: str) -> str:
        """
        Generate full path for downloaded file
        This ensures all files go to the correct directory
        """
        return os.path.join(cls.DOWNLOADS_DIR, filename)
    
    @classmethod
    def is_supported_format(cls, format_type: str) -> bool:
        """
        Check if a format is supported
        Used for validation before attempting download
        """
        return format_type.upper() in cls.SUPPORTED_FORMATS
    
    @classmethod
    def get_quality_options(cls, format_type: str) -> List[str]:
        """
        Get available quality options for a specific format
        This helps frontend show appropriate quality choices
        """
        format_type = format_type.upper()
        if cls.is_supported_format(format_type):
            return cls.SUPPORTED_FORMATS[format_type]["quality_options"]
        return []
    
    @classmethod
    def get_creator_info(cls) -> Dict[str, str]:
        """
        Return creator information for footer and about sections
        This makes it easy to display consistent creator credits
        """
        return {
            "name": cls.CREATOR,
            "github": cls.GITHUB_URL,
            "linktree": cls.LINKTREE_URL,
            "source": cls.SOURCE_REPO
        }
