# Multi-Platform Media Downloader

## Overview

This is a modern web application for downloading videos, music, and images from social media platforms. The application uses FastAPI as the backend framework with yt-dlp for media extraction, and a vanilla JavaScript frontend with TailwindCSS for styling. The project is designed as a learning exercise to explore modern web development patterns while providing a practical media downloading service.

## System Architecture

### Backend Architecture
- **Framework**: FastAPI (Python) for high-performance async web server
- **Media Processing**: yt-dlp library for extracting media from 100+ platforms
- **File Handling**: Local filesystem storage with automatic cleanup
- **API Design**: RESTful endpoints with Pydantic models for request/response validation
- **Async Processing**: Non-blocking downloads with background task processing

### Frontend Architecture
- **Technology**: Vanilla JavaScript (ES6+) with no external frameworks
- **Styling**: TailwindCSS utility-first framework via CDN
- **UI Components**: Custom radio buttons, progress indicators, and responsive design
- **Icons**: Font Awesome for consistent iconography
- **Progressive Enhancement**: Works without JavaScript for basic functionality

## Key Components

### Core Files
- **main.py**: FastAPI application entry point with API endpoints
- **downloader.py**: Media downloading service using yt-dlp
- **config.py**: Centralized configuration management
- **static/index.html**: Main frontend interface
- **static/script.js**: Frontend application logic
- **static/style.css**: Custom styling and animations

### API Endpoints
- File serving endpoints for static assets
- Download request endpoint for media processing
- File streaming endpoints for download delivery

### Media Processing
- URL validation and metadata extraction
- Format conversion (MP4, MP3, IMAGE)
- Quality selection with multiple options
- Progress tracking and error handling

## Data Flow

1. **User Input**: User pastes media URL and selects format/quality preferences
2. **Frontend Validation**: JavaScript validates URL format and enables download button
3. **API Request**: POST request sent to FastAPI backend with download parameters
4. **Media Extraction**: yt-dlp processes the URL and extracts media information
5. **Download Processing**: Media is downloaded and converted to requested format
6. **File Delivery**: Processed file is served to user with auto-cleanup
7. **Progress Updates**: Real-time status updates sent to frontend

## External Dependencies

### Backend Dependencies
- **FastAPI**: Web framework for building APIs
- **yt-dlp**: Media extraction library supporting 100+ platforms
- **uvicorn**: ASGI server for running FastAPI applications
- **pydantic**: Data validation using Python type annotations

### Frontend Dependencies
- **TailwindCSS**: Utility-first CSS framework (CDN)
- **Font Awesome**: Icon library (CDN)
- **No JavaScript frameworks**: Pure vanilla JavaScript implementation

### Platform Support
- YouTube, Instagram, Twitter, Pinterest, TikTok
- 100+ additional platforms supported by yt-dlp
- No API keys required for platform access

## Deployment Strategy

### Local Development
- Python 3.7+ required
- Run with `uvicorn main:app --reload` for development
- Static files served directly by FastAPI

### Production Considerations
- File size limit: 500MB maximum
- Automatic file cleanup after download
- Error handling for unsupported URLs
- Security considerations for user input validation

### Configuration Management
- Environment variables for debug mode
- Centralized settings in config.py
- Flexible quality and format options

## Changelog

- June 30, 2025. Initial setup

## User Preferences

Preferred communication style: Simple, everyday language.