from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
from pathlib import Path

app = Flask(__name__)
CORS(app)

PROJECT_ROOT = Path(__file__).resolve().parent
DATA_DIR = PROJECT_ROOT / "Data"

@app.route('/api/status', methods=['GET'])
def get_status():
    status_file = DATA_DIR / "Status.data"
    if status_file.exists():
        return jsonify({"status": status_file.read_text(encoding='utf-8').strip()})
    return jsonify({"status": "Available..."})

@app.route('/api/chat', methods=['GET'])
def get_chat():
    chatlog_file = DATA_DIR / "ChatLog.json"
    if chatlog_file.exists():
        try:
            with open(chatlog_file, 'r', encoding='utf-8') as f:
                history = json.load(f)
            return jsonify({"history": history})
        except Exception as e:
            return jsonify({"history": [], "error": str(e)})
    
    # Fallback to Responses.data if ChatLog.json doesn't exist
    responses_file = DATA_DIR / "Responses.data"
    if responses_file.exists():
        return jsonify({"history": [{"role": "system", "content": responses_file.read_text(encoding='utf-8').strip()}]})
    return jsonify({"history": []})

@app.route('/api/send', methods=['POST'])
def send_message():
    data = request.json
    message = data.get('message', '')
    if message:
        user_input_file = DATA_DIR / "UserInput.data"
        user_input_file.write_text(message, encoding='utf-8')
        return jsonify({"status": "success"})
    return jsonify({"status": "error", "message": "No message provided"}), 400

@app.route('/api/stats', methods=['GET'])
def get_stats():
    chatlog_file = DATA_DIR / "ChatLog.json"
    history = []
    if chatlog_file.exists():
        try:
            with open(chatlog_file, 'r', encoding='utf-8') as f:
                history = json.load(f)
        except:
            pass
    
    chat_count = len(history)
    user_msgs = len([m for m in history if m.get('role') == 'user'])
    assistant_msgs = len([m for m in history if m.get('role') == 'assistant'])
    
    import platform
    import psutil
    import datetime
    
    # Calculate uptime (approximate)
    boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
    now = datetime.datetime.now()
    uptime = str(now - boot_time).split('.')[0]
    
    system_info = {
        "total_chats": chat_count,
        "user_messages": user_msgs,
        "assistant_messages": assistant_msgs,
        "system_status": "Operational",
        "platform": platform.system(),
        "processor": platform.processor() or platform.machine(),
        "cpu_usage": f"{psutil.cpu_percent()}%",
        "memory_usage": f"{psutil.virtual_memory().percent}%",
        "uptime": uptime,
        "disk_usage": f"{psutil.disk_usage('/').percent}%",
        "python_version": platform.python_version(),
        "last_activity": history[-1]['content'][:50] + "..." if history else "No activity yet",
        "chat_history_preview": history[-5:] if history else []
    }
    
    return jsonify(system_info)

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    password = data.get('password', '')
    if password == "ansh@7318":
        auth_file = DATA_DIR / "Auth.data"
        auth_file.write_text("True", encoding='utf-8')
        return jsonify({"status": "success", "token": "dummy-token"})
    return jsonify({"status": "error", "message": "Invalid password"}), 401

if __name__ == '__main__':
    app.run(port=5001, debug=True)
