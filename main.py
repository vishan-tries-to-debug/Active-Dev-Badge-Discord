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
    print("🚀 Starting Discord Active Developer Badge Bot...")
    
    # Create thread for Bot A only
    bot_a_thread = threading.Thread(target=run_bot, args=("bot_a_standalone.py", 8080))

    # Start Bot A
    bot_a_thread.start()

    print("✅ Bot A started! It will now run indefinitely.")
    print("ℹ️ You can check its status by accessing:")
    print("   - Bot A: http://localhost:8080/status")
    print("📝 Don't forget to set up UptimeRobot to ping the Bot A endpoint regularly if you want uptime monitoring.")

    # Wait for Bot A to finish (should run indefinitely)
    bot_a_thread.join()

if __name__ == "__main__":
    main()
