
import subprocess
import os
import sys
import threading

def run_bot(bot_file, port=None):
    print(f"Starting {bot_file}...")
    env = os.environ.copy()
    if port:
        env["PORT"] = str(port)
    subprocess.run([sys.executable, bot_file], env=env)

def main():
    print("🚀 Starting Discord Active Developer Badge Bots...")
    
    # Create threads for each bot
    bot_a_thread = threading.Thread(target=run_bot, args=("bot_a_standalone.py", 8080))
    bot_b_thread = threading.Thread(target=run_bot, args=("botb_standalone.py", 10000))

    # Start both bots
    bot_a_thread.start()
    bot_b_thread.start()

    print("✅ Bots started! They will now run indefinitely.")
    print("ℹ️ You can check their status by accessing:")
    print("   - Bot A: http://localhost:8080/status")
    print("   - Bot B: http://localhost:10000/status")
    print("📝 Don't forget to set up UptimeRobot to ping the Bot B endpoint regularly.")

    # Wait for both bots to finish (they should run indefinitely)
    bot_a_thread.join()
    bot_b_thread.join()

if __name__ == "__main__":
    main()
