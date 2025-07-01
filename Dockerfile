# Multi-Platform Media Downloader - CapRover Deployment
# Optimized Dockerfile for production deployment with yt-dlp
# Created by: Ritu Raj Singh

# Use Python 3.11 slim image for smaller size and better performance
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Install system dependencies needed for yt-dlp and media processing
# ffmpeg: Required for audio/video conversion and processing
# curl: For health checks and API testing
# ca-certificates: For HTTPS connections
RUN apt-get update && apt-get install -y \
    ffmpeg \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Install Python dependencies directly
# Using specific versions for production stability
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \
    fastapi==0.115.14 \
    uvicorn==0.35.0 \
    yt-dlp==2025.6.25 \
    pydantic==2.11.7 \
    requests

# Copy application source code
# Copy in specific order to optimize Docker layer caching
COPY config.py .
COPY downloader.py .
COPY main.py .
COPY static/ ./static/

# Create downloads directory with proper permissions
# This ensures the app can write downloaded files
RUN mkdir -p downloads && chmod 755 downloads

# Create non-root user for security best practices
# Running as non-root reduces security risks in production
RUN useradd --create-home --shell /bin/bash app && \
    chown -R app:app /app
USER app

# Expose port 5000 (CapRover will map this to external port)
EXPOSE 5000

# Set environment variables for production
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV DEBUG=false

# Health check to ensure container is running properly
# CapRover uses this to monitor application health
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Start command using uvicorn ASGI server
# host=0.0.0.0 allows external connections
# port=5000 matches the exposed port
# workers=1 is optimal for small to medium traffic
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000", "--workers", "1"]
