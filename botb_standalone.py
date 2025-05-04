import discord
import os
from flask import Flask, jsonify
import threading
import asyncio
from discord import app_commands
import aiohttp
import json

# ===== CONFIGURATION =====
# Set Bot B token from environment variable or use a placeholder
TOKEN = os.environ.get("DISCORD_BOT_B_TOKEN", "YOUR_BOT_B_TOKEN_HERE")

# Get channel ID from environment variable or use placeholder
# To get a channel ID: Enable Developer Mode in Discord settings,
# right-click on a channel, and select "Copy ID"
TARGET_CHANNEL_ID = int(os.environ.get("DISCORD_TARGET_CHANNEL_ID", "123456789012345678"))

# Get Bot A's application ID
BOT_A_APP_ID = os.environ.get("BOT_A_APP_ID", "YOUR_BOT_A_APP_ID_HERE")

# ===== BOT SETUP =====
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# ===== FLASK APP SETUP =====
app = Flask(__name__)

# Queue to hold ping requests
ping_queue = []

async def trigger_bot_a_slash_command():
    """Trigger Bot A's slash command using Discord's API"""
    async with aiohttp.ClientSession() as session:
        # Get the command data for Bot A's ping command
        url = f"https://discord.com/api/v10/applications/{BOT_A_APP_ID}/commands"
        headers = {
            "Authorization": f"Bot {TOKEN}",
            "Content-Type": "application/json"
        }
        
        try:
            # Get the command ID
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    commands = await response.json()
                    ping_command = next((cmd for cmd in commands if cmd["name"] == "ping"), None)
                    
                    if ping_command:
                        # Trigger the command
                        command_url = f"https://discord.com/api/v10/interactions"
                        interaction_data = {
                            "type": 2,
                            "application_id": BOT_A_APP_ID,
                            "guild_id": str(client.guilds[0].id) if client.guilds else None,
                            "channel_id": str(TARGET_CHANNEL_ID),
                            "data": {
                                "name": "ping",
                                "id": ping_command["id"],
                                "type": 1
                            }
                        }
                        
                        async with session.post(command_url, headers=headers, json=interaction_data) as response:
                            if response.status == 204:
                                print("✅ Successfully triggered Bot A's slash command")
                            else:
                                print(f"❌ Failed to trigger command: {await response.text()}")
                    else:
                        print("❌ Could not find Bot A's ping command")
                else:
                    print(f"❌ Failed to get commands: {await response.text()}")
        except Exception as e:
            print(f"❌ Error triggering command: {e}")

async def process_ping_queue():
    """Process ping requests in the bot's event loop"""
    if not ping_queue:
        return  # Nothing to process

    # Get and remove the first channel ID from the queue
    channel_id = ping_queue.pop(0)

    # Don't try to ping if the bot isn't ready
    if client.user is None:
        print("⏳ Bot not ready yet, re-queuing ping request")
        ping_queue.append(channel_id)  # Put it back in the queue
        return

    print(f"🔄 Processing ping to channel {channel_id}")

    # First try the cache
    channel = client.get_channel(channel_id)

    # If not in cache, try to fetch it
    if not channel:
        try:
            print(f"🔍 Channel not in cache, fetching channel {channel_id}")
            channel = await client.fetch_channel(channel_id)
            print(f"✅ Successfully fetched channel: {channel.name}")
        except Exception as e:
            print(f"❌ Error fetching channel: {e}")

            # Try the first text channel as a fallback
            if client.guilds:
                for guild in client.guilds:
                    if guild.text_channels:
                        channel = guild.text_channels[0]
                        print(f"⚠️ Using fallback channel: {channel.name}")
                        break

    # Send the messages if we have a valid channel
    if channel:
        try:
            print(f"📤 Sending messages to channel: {channel.name}")

            # Trigger Bot A's slash command
            await trigger_bot_a_slash_command()

            # Send status message
            status_msg = await channel.send("UptimeRobot just pinged Bot B! I'm active and running! 🔵")
            print(f"✅ Sent status message")

        except Exception as e:
            print(f"❌ Error sending messages: {e}")
    else:
        print(f"❌ Could not find any valid channel to send messages to")

# ===== FLASK ROUTES =====
@app.route("/")
def ping_webhook():
    """
    This endpoint is called by Uptime Robot or similar services
    to trigger the bot to send messages to Discord
    """
    try:
        print(f"🔔 Ping webhook accessed")
        send_ping_message(TARGET_CHANNEL_ID)
        return jsonify({"status": "ping sent", "success": True})
    except Exception as e:
        print(f"❌ Ping webhook error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/status")
def status():
    try:
        if client.user is not None:
            return jsonify({
                "status": "online",
                "bot_name": str(client.user),
                "server_count": len(client.guilds)
            })
        else:
            return jsonify({"status": "waiting"}), 200
    except Exception as e:
        print(f"❌ Status check error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


# ===== HELPER FUNCTIONS =====
def send_ping_message(channel_id):
    """Queue a ping request to be processed by the bot's event loop"""
    print(f"🔄 Queuing ping to channel {channel_id}")
    ping_queue.append(channel_id)

# ===== BOT EVENTS =====
@client.event
async def on_ready():
    print(f'✅ Bot B is ready! Logged in as {client.user}')
    print(f'🏠 Bot B is in {len(client.guilds)} servers')
    
    # Sync slash commands with Discord
    try:
        synced = await tree.sync()
        print(f"🔄 Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"❌ Failed to sync commands: {e}")

    # Verify the target channel exists
    channel = client.get_channel(TARGET_CHANNEL_ID)
    if channel:
        print(f"✅ Found target channel: {channel.name} in {channel.guild.name}")
        try:
            startup_msg = await channel.send("Bot B has started and is ready to receive pings! 🔵")
            print(f"✅ Successfully sent startup message")

            # Try to send a test ping message immediately
            test_ping = await channel.send("!pingme")
            print(f"✅ Successfully sent test pingme message")

        except Exception as e:
            print(f"❌ Failed to send startup message: {e}")
    else:
        print(f"⚠️ Target channel with ID {TARGET_CHANNEL_ID} was not found!")

    # Start a task to process the ping queue regularly
    client.loop.create_task(ping_queue_processor())

async def ping_queue_processor():
    """Task that runs in the bot's event loop and processes ping requests"""
    while True:
        # Process any pending ping requests
        if ping_queue:
            await process_ping_queue()

        # Wait before checking the queue again
        await asyncio.sleep(2)

@client.event
async def on_message(message):
    # Ignore messages from other bots
    if message.author.bot:
        return

    if message.content == "!botb":
        await message.channel.send("Bot B is here! 🔵")

    if message.content == "!status":
        await message.channel.send(f"Bot B is online and listening! In {len(client.guilds)} servers.")

    if message.content == "!help":
        await message.channel.send("Available commands: !botb, !status, !help")

# ===== SLASH COMMANDS =====
@tree.command(name="ping", description="Check if Bot B is online")
async def ping_command(interaction):
    await interaction.response.send_message("Pong! Bot B is online and active 🔵")

@tree.command(name="status", description="Check Bot B's status")
async def status_command(interaction):
    await interaction.response.send_message(f"Bot B is online and in {len(client.guilds)} servers! 🔵")

@tree.command(name="help", description="Get help with Bot B's commands")
async def help_command(interaction):
    await interaction.response.send_message("Available commands: /ping, /status, /help", ephemeral=True)

# ===== START BOT =====
def start_discord_bot():
    client.run(TOKEN)

if __name__ == "__main__":
    # Create the bot thread
    bot_thread = threading.Thread(target=start_discord_bot)
    bot_thread.daemon = True

    # Start the bot thread
    bot_thread.start()

    # Get port from environment variable or use default
    port = int(os.environ.get("PORT", 10000))

    # Run the Flask app
    app.run(host='0.0.0.0', port=port)