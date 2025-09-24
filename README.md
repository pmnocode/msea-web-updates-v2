# MapleSEA Updates Watcher

A Python tool that monitors the MapleSEA updates page for new posts and sends Discord notifications when new updates are published.

## Features

- 🔍 Automatically scrapes the MapleSEA updates page
- 📱 Sends Discord notifications with update titles and links
- 💾 Tracks previously seen posts to avoid duplicate notifications
- ⏰ Configurable check intervals
- 🧪 Built-in testing and initialization commands

## Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Discord webhook**:
   - Create a webhook in your Discord server:
     - Go to Server Settings → Integrations → Webhooks
     - Click "New Webhook"
     - Choose a channel and copy the webhook URL

   - Copy the environment file:
     ```bash
     cp .env.example .env
     ```

   - Edit `.env` and add your Discord webhook URL:
     ```
     REDACTED
     ```

3. **Initialize the watcher**:
   ```bash
   python main.py init
   ```
   This marks all current posts as "seen" to prevent spam on first run.

4. **Test the webhook**:
   ```bash
   python main.py test
   ```

## Usage

### Run the watcher continuously:
```bash
python main.py run
```
This will check for updates every 30 minutes (or your configured interval).

### Manual check:
```bash
python main.py check
```
Performs a single check for new updates.

### Commands:
- `init` - Initialize storage with current posts (run this first!)
- `test` - Test Discord webhook connection
- `check` - Run a single update check
- `run` - Start the continuous watcher (default if no command specified)

## Configuration

Edit the `.env` file to customize:

- `DISCORD_WEBHOOK_URL`: Your Discord webhook URL (required)
- `CHECK_INTERVAL_MINUTES`: How often to check for updates (default: 30 minutes)

## 🚀 Deploy to GitHub Actions (Recommended)

For 24/7 automatic monitoring without keeping your PC on:

**[📖 See GITHUB_SETUP.md for complete setup guide](GITHUB_SETUP.md)**

This will run your watcher on GitHub's servers every 5 minutes, completely free!

## Running Locally

### Run in Background (PC must stay on):
```bash
# Run in background (survives terminal closing)
nohup python3 main.py run > watcher.log 2>&1 &

# Check if running
ps aux | grep main.py

# Stop it
pkill -f main.py
```

## Logs

The watcher creates a `watcher.log` file with detailed logging information. Check this file if you encounter any issues.

## Troubleshooting

1. **No notifications received**:
   - Check that your Discord webhook URL is correct
   - Run `python main.py test` to verify webhook connectivity
   - Check `watcher.log` for errors

2. **Too many notifications**:
   - Run `python main.py init` to mark current posts as seen

3. **Script stops running**:
   - Check `watcher.log` for error messages
   - Ensure stable internet connection
   - Consider using a process manager like systemd or supervisor
