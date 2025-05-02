
# Discord Active Developer Badge Bot

This template helps you easily set up two Discord bots that interact with each other to qualify for the Discord Active Developer Badge.

## How It Works

The system consists of two Discord bots:

1. **Bot A**: Responds to commands and acknowledges messages from Bot B
2. **Bot B**: Periodically sends special commands to Bot A

This interaction fulfills the Discord Developer Badge requirement of having at least one interaction with your app commands every 30 days.

## Setup Instructions

### 1. Create Discord Applications

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications)
2. Create two new applications (one for Bot A, one for Bot B)
3. For each application:
   - Go to the "Bot" tab
   - Click "Reset Token" and copy the token
   - Enable the "Message Content Intent" under Privileged Gateway Intents
   - Disable "Public Bot" if you want to keep it private

### 2. Invite Bots to Your Server

For each bot:
1. Go to OAuth2 > URL Generator
2. Select scopes: `bot` and `applications.commands`
3. Select permissions: `Send Messages`, `Read Messages/View Channels`
4. Copy the generated URL and open it in your browser
5. Select your server and authorize the bot

### 3. Configure the Bot Tokens

1. Replace the TOKEN variables in both `bot_a_standalone.py` and `botb_standalone.py` with your own bot tokens
2. In `botb_standalone.py`, update the `target_channel_id` variable with the ID of the text channel where you want the bots to interact

### 4. Deploy the Bots

#### Option 1: Deploying on Replit
- Fork this template
- Add the following secrets in the Secrets tab:
  - `DISCORD_BOT_A_TOKEN`: Your Bot A token
  - `DISCORD_BOT_B_TOKEN`: Your Bot B token
  - `DISCORD_TARGET_CHANNEL_ID`: The channel ID where bots will interact
- Click the Run button to start both bots
- Set up an Uptime Robot monitor to keep your repl alive

#### Option 2: Deploying on Railway and Render

##### Bot A on Railway:
1. Create a new project on [Railway](https://railway.app/)
2. Connect your GitHub repository
3. Add the following environment variables:
   - `DISCORD_BOT_A_TOKEN`: Your Bot A token
   - `PORT`: Set to `8080`
4. Set the start command to `python bot_a_standalone.py`

##### Bot B on Render:
1. Create a new Web Service on [Render](https://render.com/)
2. Connect your GitHub repository
3. Add the following environment variables:
   - `DISCORD_BOT_B_TOKEN`: Your Bot B token
   - `DISCORD_TARGET_CHANNEL_ID`: The channel ID where bots will interact
   - `PORT`: Set to `10000`
4. Set the start command to `python botb_standalone.py`
5. Set up a ping service (like UptimeRobot) to ping Bot B's webhook URL regularly (the URL will be provided by Render)

## Getting Your Active Developer Badge

1. Make sure both bots are running and in the same server
2. Wait for Bot B to send the `!activatebadge` command to the specified channel
3. Verify that Bot A responds with an acknowledgment
4. Visit [Discord Developer Portal](https://discord.com/developers/active-developer) after 24 hours to claim your badge

## Customizing the Bots

- Edit the commands in `bot_a_standalone.py` to customize Bot A's responses
- Modify the ping message in `botb_standalone.py` to change what Bot B sends

## Troubleshooting

- Ensure both bots have the correct permissions in your Discord server
- Check that the channel ID in the environment variables is correct
- Verify that your hosting platform is keeping the bots running 24/7
- If deploying on Railway/Render:
  - Make sure all environment variables are set correctly
  - Check that the service is running and not in a crashed state
  - For Bot B on Render, verify that UptimeRobot is correctly pinging your webhook URL

## License

This template is available under the MIT License.
