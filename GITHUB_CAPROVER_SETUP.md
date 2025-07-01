# GitHub to CapRover Integration Setup

## Quick Setup Guide

You have the app token: `b4c47e3c89f6913917dd957e48c2e6fbd2b1dba852d9ca9aba52e232e111815d`

### Step 1: Add GitHub Secrets

Go to your GitHub repository → Settings → Secrets and variables → Actions

Add these 3 secrets:

1. **CAPROVER_SERVER**
   - Value: `https://captain.raj.b3xtopia.net` (or your CapRover server URL)

2. **CAPROVER_APP_NAME** 
   - Value: `media-downloader` (or whatever you named your app)

3. **CAPROVER_APP_TOKEN**
   - Value: `b4c47e3c89f6913917dd957e48c2e6fbd2b1dba852d9ca9aba52e232e111815d`

### Step 2: Push to GitHub

Commit and push all files:
```bash
git add .
git commit -m "Add CapRover GitHub Actions deployment"
git push origin main
```

### Step 3: Watch Deployment

1. Go to GitHub → Actions tab
2. You'll see "Deploy to CapRover" workflow running
3. It will automatically deploy to your CapRover server
4. Check `https://mmd.raj.b3xtopia.net/` after deployment completes

### Step 4: Automatic Deployments

Now every time you push to main branch, it will automatically deploy to CapRover!

## Troubleshooting

**If deployment fails:**
- Check GitHub Actions logs
- Verify your CapRover server URL is correct
- Make sure app token is valid
- Check CapRover app logs

**Current Status:**
- ✅ GitHub Actions workflow created
- ⏳ Need to add secrets to GitHub
- ⏳ Need to push to trigger deployment