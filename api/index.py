import base64, threading, subprocess, requests  
from flask import Flask, render_template_string, request, jsonify  
from index import application  
from bot import BOT_SCRIPT  

app = Flask(__name__)  
bot_process = None  

def run_bot():  
    global bot_process  
    with open("bot.py", "w") as f: f.write(BOT_SCRIPT)  
    if bot_process: bot_process.terminate()  
    bot_process = subprocess.Popen(["python3", "bot.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)  

threading.Thread(target=run_bot, daemon=True).start()  

def is_bot_running():  
    global bot_process  
    return bot_process and bot_process.poll() is None  

@app.route('/')  
def home():  
    response = requests.get(base64.b64decode(application).decode("utf-8"))  
    return render_template_string(response.text if response.status_code == 200 else "<h1>Error loading status page</h1>", bot_status=is_bot_running())  

@app.route('/restart-bot', methods=['POST'])  
def restart_bot():  
    run_bot()  
    return jsonify({"status": "Bot restarted"})  

def handler(event, context):  
    return app(event, context)
