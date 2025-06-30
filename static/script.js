/**
 * Frontend JavaScript for Multi-Platform Media Downloader
 * This file handles all the user interactions and API communication
 * Created by: Ritu Raj Singh
 */

// Main application object to organize our code
const MediaDownloader = {
    // Application state
    state: {
        isDownloading: false,
        currentRequest: null
    },
    
    // DOM element references for better performance
    elements: {},
    
    // Current media info for preview
    currentMedia: null,
    
    /**
     * Initialize the application when page loads
     * This sets up all event listeners and prepares the UI
     */
    init() {
        console.log('🚀 Initializing Media Downloader...');
        
        // Cache DOM elements for better performance
        this.cacheElements();
        
        // Set up all event listeners
        this.setupEventListeners();
        
        // Initialize UI state
        this.setupUI();
        
        console.log('✅ Media Downloader ready!');
    },
    
    /**
     * Cache frequently used DOM elements
     * This prevents repeated DOM queries and improves performance
     */
    cacheElements() {
        this.elements = {
            urlInput: document.getElementById('url-input'),
            clearUrl: document.getElementById('clear-url'),
            formatRadios: document.querySelectorAll('input[name="format"]'),
            qualitySelect: document.getElementById('quality-select'),
            downloadBtn: document.getElementById('download-btn'),
            downloadText: document.getElementById('download-text'),
            loadingText: document.getElementById('loading-text'),
            progressSection: document.getElementById('progress-section'),
            progressBar: document.getElementById('progress-bar'),
            progressText: document.getElementById('progress-text'),
            resultSection: document.getElementById('result-section'),
            successResult: document.getElementById('success-result'),
            errorResult: document.getElementById('error-result'),
            fileName: document.getElementById('file-name'),
            fileSize: document.getElementById('file-size'),
            fileIcon: document.getElementById('file-icon'),
            downloadLink: document.getElementById('download-link'),
            errorMessage: document.getElementById('error-message'),
            retryBtn: document.getElementById('retry-btn'),
            downloadAnother: document.getElementById('download-another'),
            progressPercentage: document.getElementById('progress-percentage'),
            progressSpeed: document.getElementById('progress-speed'),
            mediaPreview: document.getElementById('media-preview'),
            mediaTitle: document.getElementById('media-title'),
            mediaInfo: document.getElementById('media-info'),
            mediaDuration: document.getElementById('media-duration'),
            mediaSize: document.getElementById('media-size'),
            previewThumbnail: document.getElementById('preview-thumbnail')
        };
    },
    
    /**
     * Set up all event listeners for user interactions
     * This handles clicks, input changes, and other user actions
     */
    setupEventListeners() {
        // URL input events
        this.elements.urlInput.addEventListener('input', () => {
            this.handleUrlInputChange();
        });
        
        this.elements.urlInput.addEventListener('paste', () => {
            // Small delay to let the paste complete
            setTimeout(() => this.handleUrlInputChange(), 10);
        });
        
        // Clear URL button
        this.elements.clearUrl.addEventListener('click', () => {
            this.clearUrl();
        });
        
        // Format selection changes
        this.elements.formatRadios.forEach(radio => {
            radio.addEventListener('change', () => {
                this.handleFormatChange(radio.value);
            });
        });
        
        // Download button click
        this.elements.downloadBtn.addEventListener('click', () => {
            this.startDownload();
        });
        
        // Retry button click
        this.elements.retryBtn.addEventListener('click', () => {
            this.resetForm();
        });
        
        // Download another button click
        this.elements.downloadAnother.addEventListener('click', () => {
            this.resetForm();
        });
        
        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            // Enter key to start download
            if (e.key === 'Enter' && !this.state.isDownloading) {
                this.startDownload();
            }
            
            // Escape key to cancel/reset
            if (e.key === 'Escape') {
                this.resetForm();
            }
        });
    },
    
    /**
     * Initialize UI state and default selections
     * Sets up the interface with sensible defaults
     */
    setupUI() {
        // Set default format quality options
        this.updateQualityOptions('MP4');
        
        // Focus on URL input for immediate use
        this.elements.urlInput.focus();
        
        // Set up initial button state
        this.updateDownloadButton();
    },
    
    /**
     * Handle changes to the URL input field
     * Shows/hides clear button and validates input
     */
    handleUrlInputChange() {
        const url = this.elements.urlInput.value.trim();
        
        // Show/hide clear button based on input
        if (url) {
            this.elements.clearUrl.classList.remove('hidden');
        } else {
            this.elements.clearUrl.classList.add('hidden');
        }
        
        // Update download button state
        this.updateDownloadButton();
        
        // Hide any previous results when URL changes
        this.hideResults();
    },
    
    /**
     * Clear the URL input and reset related UI
     * Provides a quick way to start over
     */
    clearUrl() {
        this.elements.urlInput.value = '';
        this.elements.clearUrl.classList.add('hidden');
        this.updateDownloadButton();
        this.hideResults();
        this.elements.urlInput.focus();
    },
    
    /**
     * Handle format selection changes
     * Updates quality options based on selected format
     */
    handleFormatChange(format) {
        console.log(`📝 Format changed to: ${format}`);
        this.updateQualityOptions(format);
        this.hideResults();
    },
    
    /**
     * Update quality dropdown options based on selected format
     * Different formats have different quality options available
     */
    updateQualityOptions(format) {
        const qualitySelect = this.elements.qualitySelect;
        
        // Clear existing options
        qualitySelect.innerHTML = '';
        
        let options = [];
        
        // Define quality options for each format
        switch (format) {
            case 'MP4':
                options = [
                    { value: 'best', text: 'Best Quality' },
                    { value: '1080p', text: '1080p HD' },
                    { value: '720p', text: '720p HD' },
                    { value: '480p', text: '480p' },
                    { value: '360p', text: '360p' },
                    { value: 'worst', text: 'Smallest Size' }
                ];
                break;
                
            case 'MP3':
                options = [
                    { value: 'best', text: 'Best Quality' },
                    { value: '320k', text: '320 kbps' },
                    { value: '256k', text: '256 kbps' },
                    { value: '192k', text: '192 kbps' },
                    { value: '128k', text: '128 kbps' },
                    { value: 'worst', text: 'Smallest Size' }
                ];
                break;
                
            case 'IMAGE':
                options = [
                    { value: 'best', text: 'Original Quality' },
                    { value: 'original', text: 'Original Size' }
                ];
                break;
                
            default:
                options = [{ value: 'best', text: 'Best Quality' }];
        }
        
        // Add options to select
        options.forEach(option => {
            const optionElement = document.createElement('option');
            optionElement.value = option.value;
            optionElement.textContent = option.text;
            qualitySelect.appendChild(optionElement);
        });
    },
    
    /**
     * Update download button state based on form validation
     * Enables/disables button and updates text accordingly
     */
    updateDownloadButton() {
        const url = this.elements.urlInput.value.trim();
        const isValidUrl = url && url.startsWith('http');
        
        this.elements.downloadBtn.disabled = !isValidUrl || this.state.isDownloading;
        
        // Update button styling based on state
        if (isValidUrl && !this.state.isDownloading) {
            this.elements.downloadBtn.classList.remove('opacity-50', 'cursor-not-allowed');
        } else {
            this.elements.downloadBtn.classList.add('opacity-50', 'cursor-not-allowed');
        }
    },
    
    /**
     * Start the download process
     * Validates input, shows progress, and makes API request
     */
    async startDownload() {
        // Prevent multiple simultaneous downloads
        if (this.state.isDownloading) {
            return;
        }
        
        const url = this.elements.urlInput.value.trim();
        const format = document.querySelector('input[name="format"]:checked').value;
        const quality = this.elements.qualitySelect.value;
        
        // Validate URL
        if (!url || !url.startsWith('http')) {
            this.showError('Please enter a valid URL starting with http:// or https://');
            return;
        }
        
        console.log(`🎬 Starting download: ${url} as ${format} (${quality})`);
        
        // Update UI to show download in progress
        this.state.isDownloading = true;
        this.updateDownloadButton();
        this.showProgress();
        this.hideResults();
        
        try {
            // First, get media info for preview
            await this.getMediaPreview(url, format, quality);
            
            // Use streaming download for no data persistence
            const downloadUrl = '/api/stream-download';
            const requestBody = {
                url: url,
                format: format,
                quality: quality
            };
            
            // Create a form and submit to trigger download
            const form = document.createElement('form');
            form.method = 'POST';
            form.action = downloadUrl;
            form.style.display = 'none';
            
            // Add form data
            Object.keys(requestBody).forEach(key => {
                const input = document.createElement('input');
                input.type = 'hidden';
                input.name = key;
                input.value = requestBody[key];
                form.appendChild(input);
            });
            
            document.body.appendChild(form);
            
            // Try the API call first to validate
            const response = await fetch('/api/download', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(requestBody)
            });
            
            const result = await response.json();
            
            if (result.success) {
                // Download succeeded - trigger actual download
                console.log('✅ Download successful, starting stream...');
                
                // Use the download link approach for better user experience
                const downloadLink = document.createElement('a');
                downloadLink.href = result.download_url;
                downloadLink.download = result.filename;
                downloadLink.style.display = 'none';
                document.body.appendChild(downloadLink);
                downloadLink.click();
                document.body.removeChild(downloadLink);
                
                this.showSuccess(result);
                
                // Auto-reload after successful download (with delay)
                setTimeout(() => {
                    this.showAutoReloadMessage();
                }, 3000);
            } else {
                // Download failed
                console.error('❌ Download failed:', result.message);
                this.showError(result.message);
            }
            
        } catch (error) {
            // Network or other error
            console.error('🚨 Download error:', error);
            this.showError('Network error. Please check your connection and try again.');
        } finally {
            // Reset download state
            this.state.isDownloading = false;
            this.updateDownloadButton();
            this.hideProgress();
        }
    },
    
    /**
     * Get media preview information before download
     * Shows thumbnail and metadata for better user experience
     */
    async getMediaPreview(url, format, quality) {
        try {
            // Show basic preview first
            this.elements.mediaPreview.classList.remove('hidden');
            this.elements.mediaTitle.textContent = 'Extracting media information...';
            this.elements.mediaInfo.textContent = 'Please wait while we analyze the URL';
            
            // For now, we'll simulate getting basic info
            // In a real implementation, you'd make an API call to get metadata
            const urlObj = new URL(url);
            const platform = this.getPlatformFromURL(urlObj.hostname);
            
            this.elements.mediaTitle.textContent = `Media from ${platform}`;
            this.elements.mediaInfo.textContent = `Format: ${format} | Quality: ${quality}`;
            this.elements.mediaDuration.textContent = 'Analyzing...';
            this.elements.mediaSize.textContent = 'Calculating...';
            
            // Update thumbnail based on platform
            this.updatePreviewThumbnail(platform, format);
            
        } catch (error) {
            console.log('Preview extraction failed:', error);
            // Continue without preview
        }
    },
    
    /**
     * Get platform name from URL hostname
     * Identifies the source platform for better preview
     */
    getPlatformFromURL(hostname) {
        if (hostname.includes('youtube.com') || hostname.includes('youtu.be')) return 'YouTube';
        if (hostname.includes('instagram.com')) return 'Instagram';
        if (hostname.includes('twitter.com') || hostname.includes('x.com')) return 'Twitter/X';
        if (hostname.includes('pinterest.com')) return 'Pinterest';
        if (hostname.includes('tiktok.com')) return 'TikTok';
        if (hostname.includes('facebook.com')) return 'Facebook';
        return 'Unknown Platform';
    },
    
    /**
     * Update preview thumbnail based on platform and format
     * Shows appropriate icon for the media type
     */
    updatePreviewThumbnail(platform, format) {
        const iconMap = {
            'YouTube': 'fab fa-youtube text-red-400',
            'Instagram': 'fab fa-instagram text-pink-400',
            'Twitter/X': 'fab fa-twitter text-blue-400',
            'Pinterest': 'fab fa-pinterest text-red-400',
            'TikTok': 'fab fa-tiktok text-gray-300',
            'Facebook': 'fab fa-facebook text-blue-600'
        };
        
        const formatMap = {
            'MP4': 'fas fa-video text-blue-400',
            'MP3': 'fas fa-music text-green-400',
            'IMAGE': 'fas fa-image text-purple-400'
        };
        
        const icon = iconMap[platform] || formatMap[format] || 'fas fa-download text-gray-400';
        this.elements.previewThumbnail.innerHTML = `<i class="${icon} text-2xl"></i>`;
    },

    /**
     * Show download progress UI
     * Displays progress bar and updates status text
     */
    showProgress() {
        // Show progress section
        this.elements.progressSection.classList.remove('hidden');
        
        // Switch button text to loading state
        this.elements.downloadText.classList.add('hidden');
        this.elements.loadingText.classList.remove('hidden');
        
        // Enhanced progress tracking with percentage and speed
        let progress = 0;
        let startTime = Date.now();
        
        const progressInterval = setInterval(() => {
            progress += Math.random() * 12;
            if (progress > 95) {
                progress = 95; // Stop at 95% until actual completion
                clearInterval(progressInterval);
            }
            
            // Update progress bar and percentage
            this.elements.progressBar.style.width = `${progress}%`;
            this.elements.progressPercentage.textContent = `${Math.round(progress)}%`;
            
            // Calculate estimated speed
            const elapsed = (Date.now() - startTime) / 1000;
            const speed = elapsed > 0 ? (progress / elapsed).toFixed(1) : '0';
            this.elements.progressSpeed.textContent = `${speed}%/s`;
            
            // Update progress text based on current stage
            if (progress < 20) {
                this.elements.progressText.textContent = 'Analyzing media URL...';
            } else if (progress < 40) {
                this.elements.progressText.textContent = 'Extracting media information...';
            } else if (progress < 70) {
                this.elements.progressText.textContent = 'Downloading media file...';
            } else if (progress < 95) {
                this.elements.progressText.textContent = 'Processing and optimizing...';
            } else {
                this.elements.progressText.textContent = 'Finalizing download...';
            }
        }, 300);
        
        // Store interval reference for cleanup
        this.state.progressInterval = progressInterval;
    },
    
    /**
     * Hide download progress UI
     * Cleans up progress display and resets button
     */
    hideProgress() {
        // Hide progress section
        this.elements.progressSection.classList.add('hidden');
        
        // Reset button text
        this.elements.downloadText.classList.remove('hidden');
        this.elements.loadingText.classList.add('hidden');
        
        // Clear progress interval
        if (this.state.progressInterval) {
            clearInterval(this.state.progressInterval);
            this.state.progressInterval = null;
        }
        
        // Complete progress bar
        this.elements.progressBar.style.width = '100%';
        this.elements.progressPercentage.textContent = '100%';
        
        // Hide media preview
        this.elements.mediaPreview.classList.add('hidden');
    },
    
    /**
     * Show successful download result
     * Displays download link and file information
     */
    showSuccess(result) {
        // Hide other result states
        this.elements.errorResult.classList.add('hidden');
        
        // Update file information
        this.elements.fileName.textContent = result.filename;
        this.elements.fileSize.textContent = this.formatFileSize(result.size || 0);
        
        // Set appropriate file icon based on format
        const format = document.querySelector('input[name="format"]:checked').value;
        this.updateFileIcon(format);
        
        // Set download link
        this.elements.downloadLink.href = result.download_url;
        this.elements.downloadLink.download = result.filename;
        
        // Show success result
        this.elements.successResult.classList.remove('hidden');
        this.elements.resultSection.classList.remove('hidden');
        
        // Scroll to result
        this.elements.resultSection.scrollIntoView({ 
            behavior: 'smooth', 
            block: 'nearest' 
        });
    },
    
    /**
     * Show error result
     * Displays error message and retry option
     */
    showError(message) {
        // Hide other result states
        this.elements.successResult.classList.add('hidden');
        
        // Set error message
        this.elements.errorMessage.textContent = message;
        
        // Show error result
        this.elements.errorResult.classList.remove('hidden');
        this.elements.resultSection.classList.remove('hidden');
        
        // Scroll to result
        this.elements.resultSection.scrollIntoView({ 
            behavior: 'smooth', 
            block: 'nearest' 
        });
    },
    
    /**
     * Show auto-reload message after successful download
     * Gives user option to start fresh
     */
    showAutoReloadMessage() {
        if (this.elements.successResult && !this.elements.successResult.classList.contains('hidden')) {
            // Create auto-reload notification
            const notification = document.createElement('div');
            notification.className = 'mt-4 p-3 bg-blue-500/20 border border-blue-500/30 rounded-lg text-center';
            notification.innerHTML = `
                <p class="text-blue-300 text-sm mb-2">
                    <i class="fas fa-check-circle mr-2"></i>
                    Download completed successfully!
                </p>
                <p class="text-blue-200 text-xs">
                    The form will reset in <span id="countdown">5</span> seconds for your next download
                </p>
            `;
            
            // Insert notification
            this.elements.successResult.appendChild(notification);
            
            // Countdown timer
            let countdown = 5;
            const countdownElement = notification.querySelector('#countdown');
            
            const countdownInterval = setInterval(() => {
                countdown--;
                countdownElement.textContent = countdown;
                
                if (countdown <= 0) {
                    clearInterval(countdownInterval);
                    this.resetForm();
                }
            }, 1000);
        }
    },

    /**
     * Hide all result sections
     * Cleans up the UI when starting a new operation
     */
    hideResults() {
        this.elements.resultSection.classList.add('hidden');
        this.elements.successResult.classList.add('hidden');
        this.elements.errorResult.classList.add('hidden');
        this.elements.mediaPreview.classList.add('hidden');
    },
    
    /**
     * Reset the form to initial state
     * Clears all inputs and results for a fresh start
     */
    resetForm() {
        // Clear URL input
        this.clearUrl();
        
        // Reset to default format
        document.querySelector('input[name="format"][value="MP4"]').checked = true;
        this.updateQualityOptions('MP4');
        
        // Hide all result sections
        this.hideResults();
        this.hideProgress();
        
        // Reset download state
        this.state.isDownloading = false;
        this.updateDownloadButton();
        
        // Focus on URL input
        this.elements.urlInput.focus();
    },
    
    /**
     * Update file icon based on format type
     * Shows appropriate icon for the downloaded file type
     */
    updateFileIcon(format) {
        const iconMap = {
            'MP4': 'fas fa-video',
            'MP3': 'fas fa-music',
            'IMAGE': 'fas fa-image'
        };
        
        this.elements.fileIcon.className = iconMap[format] || 'fas fa-file';
    },
    
    /**
     * Format file size for human-readable display
     * Converts bytes to appropriate units (KB, MB, GB)
     */
    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }
};

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    MediaDownloader.init();
});

// Handle page visibility changes to pause/resume when tab is hidden
document.addEventListener('visibilitychange', () => {
    if (document.hidden && MediaDownloader.state.isDownloading) {
        console.log('📱 Tab hidden during download - continuing in background');
    }
});

// Export for potential testing or external use
window.MediaDownloader = MediaDownloader;
