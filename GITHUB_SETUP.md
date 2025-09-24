# GitHub Actions Setup Guide

This guide will help you deploy your MapleSEA updates watcher to run automatically on GitHub's servers every 5 minutes - completely free!

## 🚀 Quick Setup

### 1. Create a GitHub Repository

1. Go to [GitHub.com](https://github.com) and sign in
2. Click the **"+"** button → **"New repository"**
3. Repository name: `msea-updates-watcher` (or any name you prefer)
4. Set to **Public** (required for free GitHub Actions minutes)
5. ✅ Check **"Add a README file"**
6. Click **"Create repository"**

### 2. Upload Your Code

**Option A: Using GitHub Web Interface**
1. In your new repository, click **"uploading an existing file"**
2. Drag and drop ALL files from your local `msea-updates-watcher` folder
3. Write commit message: "Initial commit - MapleSEA watcher"
4. Click **"Commit changes"**

**Option B: Using Git (if you have it installed)**
```bash
cd /mnt/c/Users/User/Documents/msea-updates-watcher
git init
git add .
git commit -m "Initial commit - MapleSEA watcher"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/msea-updates-watcher.git
git push -u origin main
```

### 3. Add Discord Webhook as Secret

1. In your repository, go to **Settings** → **Secrets and variables** → **Actions**
2. Click **"New repository secret"**
3. Name: `DISCORD_WEBHOOK_URL`
4. Value: `https://discord.com/api/webhooks/1420396666661507137/iCBawWybm-GQlQNENYqA5AxbdzWjf190NCYlkMCriZ-IJa3Oc5syVidZruZ2twk_Q_uO`
5. Click **"Add secret"**

### 4. Enable GitHub Actions

1. Go to **Actions** tab in your repository
2. If prompted, click **"I understand my workflows, go ahead and enable them"**
3. You should see the "MapleSEA Updates Watcher" workflow

### 5. Initialize Storage (Important!)

1. Go to **Actions** tab → **MapleSEA Updates Watcher**
2. Click **"Run workflow"** → **"Run workflow"** (green button)
3. Wait for it to complete (first run will send notifications for all current posts)
4. Check your Discord - you should see notifications!

## 🎯 How It Works

- **Automatic**: Runs every 5 minutes, 24/7
- **Free**: GitHub provides 2,000 free Action minutes/month (you'll use ~8,640 minutes/month)
- **Persistent**: Storage is maintained between runs using GitHub artifacts
- **Reliable**: GitHub's servers are very stable

## 📊 Monitoring

### Check if it's working:
1. Go to **Actions** tab in your repository
2. You'll see runs every 5 minutes
3. Click on any run to see logs
4. Green ✅ = successful, Red ❌ = failed

### Troubleshooting:
- **No Discord notifications**: Check that your webhook URL secret is correct
- **Workflow not running**: Make sure repository is public and Actions are enabled
- **Errors in logs**: Check the workflow run details for specific error messages

## 🔧 Customization

### Change Check Interval:
Edit `.github/workflows/watcher.yml`, line 6:
```yaml
- cron: '*/10 * * * *'  # Every 10 minutes
- cron: '0 * * * *'     # Every hour
- cron: '*/30 * * * *'  # Every 30 minutes
```

### Update Discord Webhook:
1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Click on `DISCORD_WEBHOOK_URL` → **Update**
3. Enter new webhook URL

## 💡 Benefits vs Local Running

| Local PC | GitHub Actions |
|----------|----------------|
| Only when PC is on | 24/7 automatic |
| Uses your internet | Uses GitHub's servers |
| Terminal must stay open | Completely hands-off |
| Free but limited | Free with generous limits |

## 🎉 You're All Set!

Once set up, your watcher will:
- ✅ Run automatically every 5 minutes
- ✅ Send Discord notifications for new posts
- ✅ Send Discord notifications for updated posts
- ✅ Never miss an update, even when you're asleep!

Check your Discord server - you should start seeing MapleSEA update notifications! 🍁