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
            retryBtn: document.getElementById('retry-btn')
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
            // Make API request to download media
            const response = await fetch('/api/download', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    url: url,
                    format: format,
                    quality: quality
                })
            });
            
            const result = await response.json();
            
            if (result.success) {
                // Download succeeded
                console.log('✅ Download successful:', result);
                this.showSuccess(result);
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
     * Show download progress UI
     * Displays progress bar and updates status text
     */
    showProgress() {
        // Show progress section
        this.progressSection.classList.remove('hidden');
        
        // Switch button text to loading state
        this.elements.downloadText.classList.add('hidden');
        this.elements.loadingText.classList.remove('hidden');
        
        // Animate progress bar (simulated progress since yt-dlp doesn't provide real-time progress)
        let progress = 0;
        const progressInterval = setInterval(() => {
            progress += Math.random() * 15;
            if (progress > 90) {
                progress = 90; // Stop at 90% until actual completion
                clearInterval(progressInterval);
            }
            
            this.elements.progressBar.style.width = `${progress}%`;
            
            // Update progress text based on current stage
            if (progress < 30) {
                this.elements.progressText.textContent = 'Analyzing media URL...';
            } else if (progress < 60) {
                this.elements.progressText.textContent = 'Downloading media file...';
            } else if (progress < 90) {
                this.elements.progressText.textContent = 'Processing download...';
            } else {
                this.elements.progressText.textContent = 'Finalizing...';
            }
        }, 200);
        
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
     * Hide all result sections
     * Cleans up the UI when starting a new operation
     */
    hideResults() {
        this.elements.resultSection.classList.add('hidden');
        this.elements.successResult.classList.add('hidden');
        this.elements.errorResult.classList.add('hidden');
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
