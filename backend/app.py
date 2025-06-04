from flask import Flask, request, render_template_string
import datetime
import os

app = Flask(__name__)

# Interface with coloring and Faizan's name
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Faizan™ IP Tracker</title>
    <style>
        body { background-color: #0f0f0f; color: #00ff99; font-family: monospace; text-align: center; padding: 20px; }
        h1 { color: #00ffff; }
        .info { border: 1px solid #00ff99; padding: 10px; margin: 20px auto; width: 90%; max-width: 600px; background: #1a1a1a; border-radius: 8px; }
    </style>
</head>
<body>
    <h1>Faizan™ IP Tracker</h1>
    <p>Welcome to Faizan's Ethical IP Tracking Tool.</p>
    <div class="info">
        <h2>📍 Your Info:</h2>
        <p><strong>IP Address:</strong> {{ ip }}</p>
        <p><strong>User-Agent:</strong> {{ ua }}</p>
        <p><strong>Date/Time:</strong> {{ time }}</p>
    </div>
</body>
</html>
"""

# Save to logs
def save_log(ip, ua):
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    with open(f"{log_dir}/victim_log.txt", "a") as f:
        f.write(f"[{datetime.datetime.now()}] IP: {ip} | UA: {ua}\n")

@app.route("/")
def index():
    ip = request.remote_addr
    ua = request.headers.get('User-Agent')
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    save_log(ip, ua)
    return render_template_string(html_template, ip=ip, ua=ua, time=time)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
