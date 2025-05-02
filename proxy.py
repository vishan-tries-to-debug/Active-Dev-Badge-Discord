
from flask import Flask, redirect, request, jsonify
import requests
import threading
import json

app = Flask(__name__)

@app.route('/')
def home():
    # Get status of both bots
    bot_a_status = get_bot_a_status()
    bot_b_status = get_bot_b_status()
    
    try:
        bot_a_data = json.loads(bot_a_status)
        bot_a_state = bot_a_data.get("status", "unknown")
        bot_a_name = bot_a_data.get("bot_name", "Unknown")
    except:
        bot_a_state = "offline"
        bot_a_name = "Bot A"
    
    try:
        bot_b_data = json.loads(bot_b_status)
        bot_b_state = bot_b_data.get("status", "unknown")
        bot_b_name = bot_b_data.get("bot_name", "Unknown")
    except:
        bot_b_state = "offline"
        bot_b_name = "Bot B"
    
    status_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Discord Bots Status Page</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }}
            h1 {{ color: #5865F2; }}
            .status {{ margin: 20px 0; padding: 15px; border-radius: 5px; }}
            .bot {{ margin-bottom: 20px; padding: 15px; border-radius: 5px; border: 1px solid #ddd; }}
            .online {{ color: green; }}
            .offline, .error {{ color: red; }}
            .waiting {{ color: orange; }}
            .unknown {{ color: gray; }}
            .refresh {{ margin-top: 30px; padding: 10px; background: #5865F2; color: white; 
                      border: none; border-radius: 5px; cursor: pointer; }}
        </style>
        <meta http-equiv="refresh" content="30">
    </head>
    <body>
        <h1>Discord Bots Status Dashboard</h1>
        
        <div class="bot">
            <h2>{bot_a_name}</h2>
            <p>Status: <span class="{bot_a_state}">{bot_a_state.upper()}</span></p>
        </div>
        
        <div class="bot">
            <h2>{bot_b_name}</h2>
            <p>Status: <span class="{bot_b_state}">{bot_b_state.upper()}</span></p>
        </div>
        
        <button class="refresh" onclick="location.reload()">Refresh Status</button>
        <p><small>Page auto-refreshes every 30 seconds</small></p>
    </body>
    </html>
    """
    return status_html

def get_bot_a_status():
    # Try primary port first, then fallback port
    try:
        response = requests.get('http://127.0.0.1:8080/bot-a', timeout=3)
        return response.text
    except:
        try:
            response = requests.get('http://127.0.0.1:8082/bot-a', timeout=3)
            return response.text
        except Exception as e:
            print(f"Bot A error: {e}")
            return json.dumps({"status": "offline", "message": "Bot A is not responding"})

def get_bot_b_status():
    # Try primary port first, then fallback port
    try:
        response = requests.get('http://127.0.0.1:8081/bot-b', timeout=3)
        return response.text
    except:
        try:
            response = requests.get('http://127.0.0.1:8083/bot-b', timeout=3)
            return response.text
        except Exception as e:
            print(f"Bot B error: {e}")
            return json.dumps({"status": "offline", "message": "Bot B is not responding"})

@app.route('/bot-a')
def bot_a():
    return get_bot_a_status()

@app.route('/bot-b')
def bot_b():
    return get_bot_b_status()

@app.route('/ping-test')
def ping_test():
    """Test endpoint that directly pings Bot B's webhook"""
    try:
        # Increased timeout for reliability
        response = requests.get('http://127.0.0.1:8081/', timeout=10)
        return f"""
        <html>
        <head>
            <title>Ping Test</title>
            <meta http-equiv="refresh" content="5;url=/discord-status">
        </head>
        <body>
            <h1>Ping Test Result</h1>
            <p>Status code: {response.status_code}</p>
            <p>Response: {response.text}</p>
            <p><strong>Redirecting to Discord status page in 5 seconds to check if bots are online...</strong></p>
            <p><a href="/discord-status">Check Discord Status</a></p>
        </body>
        </html>
        """
    except Exception as e:
        return f"Error pinging Bot B: {str(e)}"

@app.route('/discord-status')
def discord_status():
    """Test endpoint that checks both bots' Discord connection status"""
    try:
        bot_a_response = requests.get('http://127.0.0.1:8080/bot-a', timeout=3).json()
        bot_b_response = requests.get('http://127.0.0.1:8081/bot-b', timeout=3).json()
        
        return f"""
        <html>
        <head>
            <title>Discord Connection Status</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .status {{ padding: 10px; margin: 10px 0; border-radius: 5px; }}
                .online {{ background-color: #d4edda; color: #155724; }}
                .offline {{ background-color: #f8d7da; color: #721c24; }}
                .waiting {{ background-color: #fff3cd; color: #856404; }}
            </style>
        </head>
        <body>
            <h1>Discord Connection Status</h1>
            <div class="status {bot_a_response.get('status', 'offline')}">
                <h2>Bot A Status: {bot_a_response.get('status', 'offline')}</h2>
                <p>Bot name: {bot_a_response.get('bot_name', 'Unknown')}</p>
            </div>
            <div class="status {bot_b_response.get('status', 'offline')}">
                <h2>Bot B Status: {bot_b_response.get('status', 'offline')}</h2>
                <p>Bot name: {bot_b_response.get('bot_name', 'Unknown')}</p>
            </div>
            <button onclick="location.href='/test-channel'">Test Channel Access</button>
        </body>
        </html>
        """
    except Exception as e:
        return f"Error checking Discord status: {str(e)}"

def run():
    # Use only port 5000 as the primary entry point
    try:
        app.run(host='0.0.0.0', port=5000)
    except OSError:
        print("Port 5000 is busy, trying port 7000...")
        app.run(host='0.0.0.0', port=7000)

if __name__ == "__main__":
    t = threading.Thread(target=run)
    t.start()
