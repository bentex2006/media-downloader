# CapRover Deployment Guide
## Multi-Platform Media Downloader

This guide will help you deploy the Media Downloader app to your CapRover server.

### Prerequisites
- CapRover server running and accessible
- CapRover CLI installed on your machine
- Git repository with this project code

### Step 1: Login to CapRover
```bash
caprover login
```
Follow the prompts to connect to your CapRover server.

### Step 2: Create New App
```bash
caprover apps:create media-downloader
```

### Step 3: Deploy the App
From your project directory, run:
```bash
caprover deploy
```

When prompted:
- **App Name**: `media-downloader`
- **Branch**: `main` (or your current branch)

### Step 4: Configure App Settings

1. **Open CapRover Dashboard**
   - Go to your CapRover web interface
   - Navigate to Apps → media-downloader

2. **App Configs**
   - **Port**: 5000 (already configured in Dockerfile)
   - **Environment Variables**: None required (all settings are in config.py)

3. **Enable HTTPS** (Recommended)
   - Go to "HTTP Settings" tab
   - Enable "HTTPS" and "Force HTTPS"
   - Enable "Websocket Support" if needed

### Step 5: Access Your App
Your app will be available at:
- HTTP: `http://media-downloader.your-caprover-domain.com`
- HTTPS: `https://media-downloader.your-caprover-domain.com`

### Monitoring and Logs
- **View Logs**: CapRover Dashboard → Apps → media-downloader → App Logs
- **App Metrics**: Available in the monitoring section
- **Health Check**: The app includes automatic health monitoring

### Troubleshooting

#### Common Issues:
1. **Build Fails**
   - Check that all files are committed to git
   - Verify Dockerfile syntax

2. **App Won't Start**
   - Check logs in CapRover dashboard
   - Verify port 5000 is properly exposed

3. **Downloads Not Working**
   - Ensure ffmpeg is installed (included in Dockerfile)
   - Check yt-dlp compatibility with target sites

#### Performance Optimization:
- **Memory**: Recommend at least 512MB RAM
- **CPU**: 1 vCPU should be sufficient for moderate usage
- **Storage**: Downloads are auto-deleted, minimal storage needed

### Security Notes
- App runs as non-root user for security
- No persistent data storage (files auto-delete)
- HTTPS strongly recommended for production
- No API keys or secrets required

### Support
For issues with:
- **CapRover**: Check CapRover documentation
- **App Functionality**: Review app logs and GitHub repository
- **Media Downloads**: Verify URL compatibility with yt-dlp

---
**Created by**: Ritu Raj Singh  
**Project**: Multi-Platform Media Downloader  
**Repository**: [GitHub Link](https://github.com/bentex2006/media-downloader)