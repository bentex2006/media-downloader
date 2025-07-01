#!/bin/bash
# CapRover Deployment Script for Multi-Platform Media Downloader
# This script automates the deployment process to CapRover
# Created by: Ritu Raj Singh

set -e  # Exit on any error

echo "🚀 Starting CapRover deployment for Media Downloader..."

# Check if CapRover CLI is installed
if ! command -v caprover &> /dev/null; then
    echo "❌ CapRover CLI not found. Please install it first:"
    echo "npm install -g caprover"
    exit 1
fi

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "❌ This is not a git repository. Please initialize git first:"
    echo "git init"
    echo "git add ."
    echo "git commit -m 'Initial commit'"
    exit 1
fi

# Check if all files are committed
if ! git diff-index --quiet HEAD --; then
    echo "⚠️  You have uncommitted changes. Please commit them first:"
    echo "git add ."
    echo "git commit -m 'Prepare for deployment'"
    exit 1
fi

# Get app name from user
read -p "Enter your CapRover app name (default: media-downloader): " APP_NAME
APP_NAME=${APP_NAME:-media-downloader}

echo "📦 Deploying app: $APP_NAME"

# Deploy to CapRover
echo "🔄 Starting deployment..."
caprover deploy --appName "$APP_NAME"

echo "✅ Deployment completed!"
echo ""
echo "📱 Your app should be available at:"
echo "https://$APP_NAME.your-caprover-domain.com"
echo ""
echo "🔧 Next steps:"
echo "1. Check app logs in CapRover dashboard"
echo "2. Enable HTTPS in app settings"
echo "3. Test the application functionality"
echo ""
echo "📚 For troubleshooting, see CAPROVER_DEPLOYMENT.md"