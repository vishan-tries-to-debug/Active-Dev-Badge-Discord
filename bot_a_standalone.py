import discord
import os
from flask import Flask, jsonify
import threading

# ===== CONFIGURATION =====
# Set Bot A token from environment variable or use a placeholder
TOKEN = os.environ.get("DISCORD_BOT_A_TOKEN", "YOUR_BOT_A_TOKEN_HERE")

# ===== BOT SETUP =====
intents = discord.Intents.default()
intents.message_content = True  # Required to read message content

client = discord.Client(intents=intents)
from discord import app_commands
tree = app_commands.CommandTree(client)

# ===== FLASK APP SETUP =====
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot A is operational. This endpoint is used for status monitoring."

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
        print(f"Bot A status check error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

# ===== BOT EVENTS =====
@client.event
async def on_ready():
    print(f'✅ Bot A is ready! Logged in as {client.user}')
    print(f'🏠 Bot A is in {len(client.guilds)} servers')
    
    # Sync slash commands with Discord
    try:
        synced = await tree.sync()
        print(f"🔄 Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"❌ Failed to sync commands: {e}")

@client.event
async def on_message(message):
    # Ignore messages from other bots
    if message.author.bot:
        return
    
    # Handle user commands
    if message.content == "!status":
        await message.channel.send(f"Bot A is online and listening! In {len(client.guilds)} servers.")
        
    if message.content == "!help":
        await message.channel.send("Available commands: !status, !help, and /ping")

# ===== SLASH COMMANDS =====
@tree.command(name="ping", description="Check if Bot A is online")
async def ping_command(interaction):
    # Send response
    await interaction.response.send_message("Pong! Bot A is online and active 🟢")
    
    # Log the interaction
    print(f"✅ Received /ping command from {interaction.user.name} in {interaction.guild.name}")
    
    # Log to a file for tracking Active Developer Badge qualification
    with open("interaction_log.txt", "a") as f:
        f.write(f"{interaction.created_at.isoformat()},{interaction.user.name},{interaction.guild.name}\n")

@tree.context_menu(name="Highlight Message")
async def highlight_message(interaction, message: discord.Message):
    await interaction.response.send_message(f"Highlighted message: '{message.content}'", ephemeral=True)
    
    # Log the interaction
    print(f"✅ Received highlight command from {interaction.user.name} in {interaction.guild.name}")
    
    # Log to a file for tracking Active Developer Badge qualification
    with open("interaction_log.txt", "a") as f:
        f.write(f"{interaction.created_at.isoformat()},{interaction.user.name},{interaction.guild.name},highlight\n")

# ===== START BOT =====
def start_discord_bot():
    client.run(TOKEN)

bot_thread = threading.Thread(target=start_discord_bot)
bot_thread.daemon = True

if __name__ == "__main__":
    if not os.environ.get('BOT_STARTED_A'):
        bot_thread.start()
        os.environ['BOT_STARTED_A'] = 'true'
    
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
