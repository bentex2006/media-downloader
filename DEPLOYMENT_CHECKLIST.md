# CapRover Deployment Checklist
## Getting Your Media Downloader Live

Since you're seeing the CapRover placeholder page, here's what needs to be done:

### Step 1: Commit the Files ✅
You need to commit the deployment files to git:

```bash
git add .
git commit -m 'Add CapRover deployment files'
git push origin main
```

### Step 2: Check CapRover App Status
In your CapRover dashboard:

1. **Go to Apps** → **media-downloader** (or whatever you named it)
2. **Check App Status** - it should show "Not Built" or "Failed"
3. **Check Build Logs** for any errors

### Step 3: Deploy Options

**Option A: Using the Script**
```bash
./deploy.sh
```

**Option B: Manual CapRover CLI**
```bash
caprover login
caprover deploy --appName media-downloader
```

**Option C: Git Integration (Recommended)**
1. In CapRover dashboard → Apps → media-downloader
2. Go to **Deployment** tab
3. Connect your Git repository
4. Set branch to `main`
5. Click **Force Rebuild**

### Step 4: Troubleshooting Common Issues

**If Build Fails:**
- Check that all files are committed to git
- Verify your git repository is accessible
- Check build logs in CapRover dashboard

**If App Won't Start:**
- Check app logs in CapRover dashboard
- Verify port 5000 is configured
- Check if app has enough resources (512MB RAM recommended)

**Current Status:**
- Domain: https://mmd.raj.b3xtopia.net/
- Status: Showing placeholder (not deployed)
- Next Action: Complete git commit and deploy

### Step 5: After Successful Deployment
Your app should show the Media Downloader interface instead of the placeholder page.

**Test the deployment:**
- Visit your domain
- Try downloading a YouTube video
- Check that files auto-delete after download