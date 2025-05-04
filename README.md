# Discord Active Developer Badge Bot

A simple Discord bot to help you qualify for the Discord Active Developer Badge by providing a `/ping` slash command.

---

## Features
- Responds to `/ping` slash command
- Provides a `/status` HTTP endpoint for uptime monitoring
- Easy deployment on Railway

---

## 🚀 Quick Setup (Railway)

### 1. **Deploy to Railway**
- Go to [Railway](https://railway.app/)
- Click **New Project** > **Deploy from GitHub repo**
- Connect your GitHub account and select this repository

### 2. **Set Environment Variables**
- In Railway, go to your project > **Variables**
- Add:
  - `DISCORD_BOT_A_TOKEN` = *your Discord bot token*

### 3. **Set the Start Command**
- In Railway, go to **Settings** > **Deployments**
- Set the start command to:
  ```
  python bot_a_standalone.py
  ```

### 4. **Deploy**
- Click **Deploy** or **Restart** to start the bot
- Check the Railway logs to confirm the bot is running

### 5. **Invite the Bot to Your Server**
- Go to the [Discord Developer Portal](https://discord.com/developers/applications)
- Select your bot > **OAuth2** > **URL Generator**
- Scopes: `bot`, `applications.commands`
- Permissions: `Send Messages`, `Use Slash Commands`
- Copy and open the generated URL to invite the bot

---

## (Optional) Uptime Monitoring with UptimeRobot

Keep your Railway bot awake by pinging its status endpoint!

### 1. **Get Your Railway Service URL**
- In Railway, go to your deployed service
- Click the **"Open App"** button (or copy the domain shown in the service overview)
- Your URL will look like: `https://your-app-name.up.railway.app`

### 2. **Set Up UptimeRobot**
- Go to [UptimeRobot](https://uptimerobot.com/)
- Create a free account (if you don't have one)
- Click **Add New Monitor**
  - Monitor Type: **HTTP(s)**
  - Friendly Name: `Discord Bot A`
  - URL: `https://your-app-name.up.railway.app/status`
  - Monitoring Interval: 5 minutes (recommended)
- Click **Create Monitor**

UptimeRobot will now ping your bot's `/status` endpoint to keep it awake!

---

## Usage
- In your Discord server, type `/ping` and select the command from Bot A
- Use the slash command at least once every 30 days to keep your Active Developer Badge

---

## License
MIT
