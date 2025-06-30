# Multi-Platform Media Downloader

## Overview

This is a web application for downloading videos, music, and images from popular social media platforms like YouTube, Instagram, Twitter, Pinterest, and TikTok. The application provides a clean, modern interface with support for multiple formats (MP4, MP3, IMAGE) and quality options. It uses yt-dlp library for platform access without requiring API keys.

## System Architecture

The application follows a client-server architecture with a clear separation between frontend and backend:

- **Frontend**: Static HTML/CSS/JavaScript with TailwindCSS for styling
- **Backend**: FastAPI (Python) web server handling API requests
- **Download Engine**: yt-dlp library for media extraction and downloading
- **File Storage**: Local filesystem for temporary downloads

The architecture prioritizes simplicity and educational value while maintaining production-ready error handling and security considerations.

## Key Components

### Backend Components

1. **FastAPI Server (main.py)**
   - Handles API endpoints for download requests
   - Serves static files and downloaded content
   - Provides request validation using Pydantic models
   - Implements background task processing for downloads

2. **Media Downloader Service (downloader.py)**
   - Wraps yt-dlp library for media extraction
   - Handles format conversion and quality selection
   - Implements file sanitization and error handling
   - Supports async operations for better performance

3. **Configuration Management (config.py)**
   - Centralizes all application settings
   - Defines supported formats and quality options
   - Contains creator information and external links
   - Manages file size limits and directory paths

### Frontend Components

1. **User Interface (static/index.html)**
   - Responsive design using TailwindCSS
   - Dark theme with gradient effects
   - Form controls for URL input and format selection
   - Progress tracking and download status display

2. **Application Logic (static/script.js)**
   - Handles user interactions and form validation
   - Manages API communication with backend
   - Implements real-time progress updates
   - Provides error handling and user feedback

3. **Custom Styling (static/style.css)**
   - Enhanced visual effects and animations
   - Custom radio button styling
   - Responsive design improvements
   - Accessibility enhancements

## Data Flow

1. **User Input**: User pastes media URL and selects format/quality preferences
2. **Frontend Validation**: JavaScript validates URL format and required fields
3. **API Request**: Frontend sends POST request to `/download` endpoint
4. **Backend Processing**: FastAPI server validates request and initiates download
5. **Media Extraction**: yt-dlp extracts media information and downloads content
6. **File Processing**: Downloaded files are sanitized and stored in downloads directory
7. **Response**: Backend returns download URL and filename to frontend
8. **User Download**: Frontend provides direct download link to user

## External Dependencies

### Python Libraries
- **FastAPI**: Modern web framework for building APIs
- **yt-dlp**: Fork of youtube-dl with enhanced platform support
- **uvicorn**: ASGI server for running FastAPI applications
- **pydantic**: Data validation using Python type annotations

### Frontend Libraries
- **TailwindCSS**: Utility-first CSS framework via CDN
- **Font Awesome**: Icon library for UI elements
- **Native JavaScript**: No additional frontend frameworks required

### Platform Support
- YouTube, Instagram, Twitter, Pinterest, TikTok
- 100+ additional platforms supported by yt-dlp
- No API keys required for platform access

## Deployment Strategy

The application is designed for simple deployment with minimal configuration:

1. **Development**: Run locally using uvicorn server on port 5000
2. **Container Ready**: Configuration supports container deployment
3. **Static File Serving**: FastAPI serves frontend files directly
4. **File Management**: Downloads stored in local filesystem
5. **Error Handling**: Comprehensive logging and error recovery

### Configuration Options
- Debug mode controlled via environment variables
- Host binding supports container deployment (0.0.0.0)
- File size limits configurable (default 500MB)
- Download directory customizable

## Changelog
- June 30, 2025. Initial setup

## User Preferences

Preferred communication style: Simple, everyday language.