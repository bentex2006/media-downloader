"""
Media downloader service using yt-dlp
This handles the actual downloading of media from various platforms
Created by: Ritu Raj Singh
"""

import yt_dlp
import os
import asyncio
import logging
from typing import Dict, Any, Optional
from config import AppConfig
import re
import uuid

# Set up logging for download operations
logger = logging.getLogger(__name__)

class MediaDownloader:
    """
    Handles media downloading using yt-dlp library
    This class encapsulates all the download logic and error handling
    """
    
    def __init__(self):
        """
        Initialize the downloader with default settings
        Sets up the basic configuration for yt-dlp with long-term stability
        """
        # Ensure downloads directory exists
        os.makedirs(AppConfig.DOWNLOADS_DIR, exist_ok=True)
        
        # Initialize fallback user agents for rotation
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:120.0) Gecko/20100101 Firefox/120.0'
        ]
        self.current_ua_index = 0
        
        # Optimized yt-dlp options for faster downloads
        self.base_options = {
            'outtmpl': os.path.join(AppConfig.DOWNLOADS_DIR, '%(title)s.%(ext)s'),
            'noplaylist': True,  # Don't download entire playlists
            'extract_flat': False,  # Get full metadata
            'ignoreerrors': True,  # Continue on minor errors
            
            # Disable problematic features that cause fragmented downloads
            'no_part': True,  # Don't use .part files
            'retries': 5,  # Reasonable retry count
            'fragment_retries': 5,  # Fragment retry count
            'socket_timeout': 60,  # Longer timeout for stability
            'geo_bypass': True,  # Bypass geographic restrictions
            
            # Avoid HLS/DASH fragmented streams that cause range errors
            'format_sort': ['proto:http', 'proto:https'],
            
            # Quality optimizations
            'writesubtitles': False,  # Skip subtitles
            'writeautomaticsub': False,  # Skip auto-generated subs
            'writethumbnail': False,  # Skip thumbnail download
            'writeinfojson': False,  # Skip metadata file
            'embed_chapters': False,  # Skip chapters
            'embed_subs': False,  # Skip embedded subtitles
            
            # Long-term stability fixes for YouTube cookies and authentication
            'extractor_args': {
                'youtube': {
                    'player_client': ['android', 'web'],  # Use multiple clients for reliability
                    'player_skip': ['webpage'],  # Skip webpage parsing that can break
                    'comment_sort': ['top'],  # Optimize comment extraction
                    'max_comments': [0],  # Disable comments to avoid API limits
                }
            },
            
            # Additional stability options
            'age_limit': None,  # Don't restrict age-limited content
            'ignoreerrors': True,  # Continue on errors
            'no_check_certificate': False,  # Use proper SSL verification
            'prefer_ffmpeg': True,  # Prefer ffmpeg for processing
            
            # Anti-detection measures for long-term stability
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-us,en;q=0.5',
                'Accept-Encoding': 'gzip,deflate',
                'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
                'Keep-Alive': '115',
                'Connection': 'keep-alive',
            },
            
            # Bypass restrictions and rate limiting
            'sleep_interval': 1,  # Small delay between requests
            'max_sleep_interval': 5,  # Maximum sleep interval
            'sleep_interval_requests': 1,  # Sleep between subtitle requests
        }
    
    def _sanitize_filename(self, filename: str) -> str:
        """
        Clean filename to prevent issues with special characters
        This ensures downloaded files have safe names for the filesystem
        
        Args:
            filename: Original filename from yt-dlp
            
        Returns:
            Sanitized filename safe for filesystem
        """
        # Remove or replace problematic characters that cause URL encoding issues
        # This includes: <>:"/\|?*()[]{}#%&=+@!$,;'`~
        filename = re.sub(r'[<>:"/\\|?*()[\]{}#%&=+@!$,;\'`~]', '_', filename)
        filename = re.sub(r'\s+', '_', filename)  # Replace spaces with underscores
        filename = re.sub(r'_+', '_', filename)  # Replace multiple underscores with single
        filename = filename.strip('._')  # Remove leading/trailing dots and underscores
        
        # Ensure filename isn't too long
        if len(filename) > 150:
            filename = filename[:150]
        
        # Ensure filename is not empty
        if not filename:
            filename = "downloaded_media"
        
        return filename
    
    def _get_next_user_agent(self):
        """
        Get next user agent for rotation to avoid detection
        """
        user_agent = self.user_agents[self.current_ua_index]
        self.current_ua_index = (self.current_ua_index + 1) % len(self.user_agents)
        return user_agent
    
    def _get_fallback_options(self, original_options):
        """
        Get fallback yt-dlp options for when primary extraction fails
        This helps with YouTube cookies and authentication issues
        """
        fallback_options = original_options.copy()
        
        # Use different user agent
        fallback_options['http_headers']['User-Agent'] = self._get_next_user_agent()
        
        # More aggressive extractor arguments for difficult cases
        fallback_options['extractor_args'] = {
            'youtube': {
                'player_client': ['android', 'ios', 'web'],
                'player_skip': ['webpage', 'configs'],
                'skip': ['translated_subs'],
                'lang': ['en'],
                'include_live_dash': [False]
            }
        }
        
        # Remove format sorting that might be too restrictive
        if 'format_sort' in fallback_options:
            del fallback_options['format_sort']
        
        return fallback_options
    
    def _get_format_selector(self, format_type: str, quality: str) -> str:
        """
        Generate yt-dlp format selector based on user preferences
        Different formats need different selectors for optimal downloads
        
        Args:
            format_type: MP4, MP3, or IMAGE
            quality: Quality preference (best, worst, specific resolution)
            
        Returns:
            Format selector string for yt-dlp
        """
        format_type = format_type.upper()
        
        if format_type == "MP4":
            # Avoid fragmented streams completely
            if quality == "best":
                # Prefer single-file progressive downloads
                return "best[protocol^=http][ext=mp4]/best[protocol^=https][ext=mp4]/best[ext=mp4]/best"
            elif quality == "worst":
                return "worst[protocol^=http][ext=mp4]/worst[ext=mp4]/worst"
            elif quality.endswith("p"):
                # Specific resolution - avoid fragmented streams
                height = quality[:-1]
                return f"best[height<={height}][protocol^=http][ext=mp4]/best[height<={height}][ext=mp4]/best[height<={height}]"
            else:
                return "best[protocol^=http][ext=mp4]/best[ext=mp4]/best"
                
        elif format_type == "MP3":
            # Audio format selectors
            if quality == "best":
                return "bestaudio/best"
            elif quality == "worst":
                return "worstaudio/worst"
            elif quality.endswith("k"):
                # Specific bitrate like 320k, 256k
                return f"bestaudio[abr<={quality[:-1]}]/bestaudio"
            else:
                return "bestaudio/best"
                
        elif format_type == "IMAGE":
            # Image format selectors - prefer high quality images
            if quality == "best":
                return "best[ext=jpg]/best[ext=png]/best[ext=webp]/best"
            elif quality == "original":
                return "best"
            else:
                return "best[ext=jpg]/best[ext=png]/best[ext=webp]/best"
        
        # Default fallback
        return "best"
    
    def _prepare_options(self, format_type: str, quality: str) -> Dict[str, Any]:
        """
        Prepare yt-dlp options based on download format and quality
        This configures yt-dlp for the specific type of media we want
        
        Args:
            format_type: Type of media (MP4, MP3, IMAGE)
            quality: Quality preference
            
        Returns:
            Dictionary of options for yt-dlp
        """
        options = self.base_options.copy()
        format_type = format_type.upper()
        
        # Set format selector
        options['format'] = self._get_format_selector(format_type, quality)
        
        # Optimized post-processors for faster conversion
        if format_type == "MP3":
            # Fast audio extraction with optimized settings
            quality_map = {
                "best": "320",
                "320k": "320", 
                "256k": "256",
                "192k": "192", 
                "128k": "128",
                "worst": "128"
            }
            audio_quality = quality_map.get(quality, "192")
            
            options['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': audio_quality,
                'nopostoverwrites': False,  # Faster processing
            }]
            
        elif format_type == "MP4":
            # Only convert if absolutely necessary - prefer native MP4
            options['postprocessors'] = [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            }]
        
        # Add file size limit to prevent huge downloads
        options['max_filesize'] = AppConfig.MAX_FILE_SIZE
        
        return options
    
    async def download_media(self, url: str, format_type: str, quality: str = "best") -> Dict[str, Any]:
        """
        Main download function that handles the entire download process
        This is called by the FastAPI endpoint to download media
        
        Args:
            url: URL of the media to download
            format_type: Desired format (MP4, MP3, IMAGE)
            quality: Quality preference
            
        Returns:
            Dictionary with success status and file information or error message
        """
        try:
            logger.info(f"Starting download: {url} as {format_type} quality {quality}")
            
            # Validate and expand shortened URLs (like Pinterest pin.it)
            if not url:
                return {
                    "success": False,
                    "error": "Invalid URL provided"
                }
            
            # Handle Pinterest shortened URLs
            if 'pin.it' in url:
                import requests
                try:
                    # Follow redirect to get full Pinterest URL
                    response = requests.head(url, allow_redirects=True)
                    url = response.url
                    logger.info(f"Expanded Pinterest URL to: {url}")
                except Exception as e:
                    logger.warning(f"Could not expand Pinterest URL: {e}")
            
            if not url.startswith(('http://', 'https://')):
                return {
                    "success": False,
                    "error": "Invalid URL provided"
                }
            
            if not AppConfig.is_supported_format(format_type):
                return {
                    "success": False,
                    "error": f"Unsupported format: {format_type}"
                }
            
            # Prepare yt-dlp options for this specific download
            options = self._prepare_options(format_type, quality)
            
            # Generate unique filename to avoid conflicts
            unique_id = str(uuid.uuid4())[:8]
            
            # First, extract info to check if URL is valid
            with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                try:
                    logger.info("Extracting media information...")
                    info = ydl.extract_info(url, download=False)
                    
                    if not info:
                        return {
                            "success": False,
                            "error": "Could not extract media information from URL"
                        }
                    
                    # Get media title for filename
                    title = info.get('title', 'unknown')
                    title = self._sanitize_filename(title)
                    
                    # Determine file extension based on format
                    if format_type.upper() == "MP3":
                        ext = "mp3"
                    elif format_type.upper() == "MP4":
                        ext = "mp4"
                    else:
                        # For images, use original extension or default to jpg
                        ext = info.get('ext', 'jpg')
                    
                    # Create final filename with unique ID
                    filename = f"{title}_{unique_id}.{ext}"
                    filepath = os.path.join(AppConfig.DOWNLOADS_DIR, filename)
                    
                except yt_dlp.DownloadError as e:
                    logger.error(f"yt-dlp info extraction error: {str(e)}")
                    return {
                        "success": False,
                        "error": f"Failed to extract info: {str(e)}"
                    }
            
            
            options['outtmpl'] = filepath
            
            # Add progress hook for better performance tracking
            def progress_hook(d):
                if d['status'] == 'downloading':
                    speed = d.get('speed', 0)
                    if speed:
                        logger.info(f"Download speed: {speed/1024/1024:.1f} MB/s")
                elif d['status'] == 'finished':
                    logger.info(f"Download finished: {d['filename']}")
            
            options['progress_hooks'] = [progress_hook]
            
            # Try download with primary options first, then fallback if needed
            download_attempts = [options, self._get_fallback_options(options)]
            
            for attempt_num, download_options in enumerate(download_attempts, 1):
                try:
                    download_options['outtmpl'] = filepath
                    download_options['progress_hooks'] = [progress_hook]
                    
                    logger.info(f"Download attempt {attempt_num}: {filepath}")
                    
                    with yt_dlp.YoutubeDL(download_options) as ydl:
                        # Use thread pool executor with optimized settings for faster execution
                        import concurrent.futures
                        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
                            loop = asyncio.get_event_loop()
                            await loop.run_in_executor(
                                executor, 
                                lambda: ydl.download([url])
                            )
                    
                    # If we reach here, download was successful
                    break
                    
                except yt_dlp.DownloadError as e:
                    logger.warning(f"Download attempt {attempt_num} failed: {str(e)}")
                    if attempt_num >= len(download_attempts):
                        # All attempts failed
                        return {
                            "success": False,
                            "error": f"All download attempts failed. Last error: {str(e)}"
                        }
                    else:
                        logger.info(f"Trying fallback configuration...")
                        continue
                except Exception as e:
                    logger.error(f"Unexpected error in attempt {attempt_num}: {str(e)}")
                    if attempt_num >= len(download_attempts):
                        return {
                            "success": False,
                            "error": f"Download failed: {str(e)}"
                        }
                    continue
            
            # Check if file was created successfully
            if os.path.exists(filepath):
                file_size = os.path.getsize(filepath)
                logger.info(f"Download completed: {filename} ({file_size} bytes)")
                
                return {
                    "success": True,
                    "filename": filename,
                    "filepath": filepath,
                    "title": title,
                    "size": file_size
                }
            else:
                # Sometimes yt-dlp creates files with slightly different names
                # Let's check for any files created during our download
                possible_files = [f for f in os.listdir(AppConfig.DOWNLOADS_DIR) 
                                if f.startswith(title) and unique_id in f]
                
                if possible_files:
                    actual_filename = possible_files[0]
                    actual_filepath = os.path.join(AppConfig.DOWNLOADS_DIR, actual_filename)
                    file_size = os.path.getsize(actual_filepath)
                    
                    return {
                        "success": True,
                        "filename": actual_filename,
                        "filepath": actual_filepath,
                        "title": title,
                        "size": file_size
                    }
                else:
                    return {
                        "success": False,
                        "error": "Download completed but file not found"
                    }
                    
        except Exception as e:
            logger.error(f"Unexpected error during download: {str(e)}")
            return {
                "success": False,
                "error": f"An unexpected error occurred: {str(e)}"
            }
        
        except Exception as e:
            logger.error(f"Error in download_media: {str(e)}")
            return {
                "success": False,
                "error": f"Failed to process download: {str(e)}"
            }
    
    def get_supported_sites(self) -> list:
        """
        Get list of supported sites from yt-dlp
        This returns all the platforms that yt-dlp can handle
        
        Returns:
            List of supported site names
        """
        try:
            # Get extractors from yt-dlp
            extractors = yt_dlp.list_extractors()
            # Return first 50 popular ones to avoid overwhelming the user
            return [extractor.IE_NAME for extractor in extractors[:50] if hasattr(extractor, 'IE_NAME')]
        except Exception as e:
            logger.error(f"Error getting supported sites: {str(e)}")
            # Return a basic list of popular platforms
            return [
                "youtube", "instagram", "twitter", "pinterest", "tiktok", 
                "facebook", "vimeo", "dailymotion", "reddit"
            ]
    
    async def get_media_info(self, url: str) -> Dict[str, Any]:
        """
        Extract media information without downloading
        This is used for preview functionality
        
        Args:
            url: URL of the media to analyze
            
        Returns:
            Dictionary with media information or error
        """
        try:
            logger.info(f"Extracting info for: {url}")
            
            # Basic options for info extraction only
            options = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': False,
            }
            
            with yt_dlp.YoutubeDL(options) as ydl:
                try:
                    # Extract info without downloading
                    info = ydl.extract_info(url, download=False)
                    
                    if not info:
                        return {"success": False, "error": "Could not extract media information"}
                    
                    # Clean and return useful information
                    return {
                        "success": True,
                        "title": info.get('title', 'Unknown Title'),
                        "duration": self._format_duration(info.get('duration')),
                        "thumbnail": info.get('thumbnail'),
                        "platform": info.get('extractor_key', 'Unknown'),
                        "filesize": self._format_filesize(info.get('filesize')),
                        "view_count": info.get('view_count'),
                        "uploader": info.get('uploader', 'Unknown')
                    }
                    
                except yt_dlp.DownloadError as e:
                    return {"success": False, "error": f"Failed to extract info: {str(e)}"}
                    
        except Exception as e:
            logger.error(f"Error extracting media info: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def _format_duration(self, duration) -> str:
        """
        Format duration from seconds to human readable format
        """
        if not duration:
            return "Unknown"
        
        try:
            minutes, seconds = divmod(int(duration), 60)
            hours, minutes = divmod(minutes, 60)
            
            if hours > 0:
                return f"{hours}h {minutes}m {seconds}s"
            elif minutes > 0:
                return f"{minutes}m {seconds}s"
            else:
                return f"{seconds}s"
        except:
            return "Unknown"
    
    def _format_filesize(self, filesize) -> str:
        """
        Format filesize from bytes to human readable format
        """
        if not filesize:
            return "Unknown"
        
        try:
            # Convert bytes to appropriate unit
            for unit in ['B', 'KB', 'MB', 'GB']:
                if filesize < 1024.0:
                    return f"{filesize:.1f} {unit}"
                filesize /= 1024.0
            return f"{filesize:.1f} TB"
        except:
            return "Unknown"
    
    async def stream_download_media(self, url: str, format_type: str, quality: str = "best") -> Dict[str, Any]:
        """
        Stream download media directly without saving to disk
        This ensures no data persistence on the server
        
        Args:
            url: URL of the media to download
            format_type: Desired format (MP4, MP3, IMAGE)
            quality: Quality preference
            
        Returns:
            Dictionary with stream and metadata
        """
        try:
            logger.info(f"Starting stream download: {url} as {format_type}")
            
            # For now, we'll use the regular download and then stream the file
            # In a production environment, you'd implement true streaming
            result = await self.download_media(url, format_type, quality)
            
            if result["success"]:
                filepath = result["filepath"]
                filename = result["filename"]
                
                # Determine content type
                content_type = "application/octet-stream"
                if format_type.upper() == "MP4":
                    content_type = "video/mp4"
                elif format_type.upper() == "MP3":
                    content_type = "audio/mpeg"
                elif format_type.upper() == "IMAGE":
                    content_type = "image/jpeg"
                
                # Create file stream generator
                def file_generator():
                    try:
                        with open(filepath, "rb") as f:
                            while True:
                                chunk = f.read(8192)  # 8KB chunks
                                if not chunk:
                                    break
                                yield chunk
                    finally:
                        # Clean up file after streaming
                        try:
                            if os.path.exists(filepath):
                                os.remove(filepath)
                                logger.info(f"Cleaned up temporary file: {filepath}")
                        except Exception as e:
                            logger.error(f"Failed to clean up file: {e}")
                
                return {
                    "success": True,
                    "stream": file_generator(),
                    "filename": filename,
                    "content_type": content_type
                }
            else:
                return result
                
        except Exception as e:
            logger.error(f"Error in stream download: {str(e)}")
            return {"success": False, "error": str(e)}
