from flask import Flask, request, redirect, jsonify
import sqlite3
import uuid
from datetime import datetime

app = Flask(__name__)
DB_NAME = "db.sqlite3"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS visits (
        id TEXT PRIMARY KEY,
        ip TEXT,
        user_agent TEXT,
        timestamp TEXT
    )''')
    conn.commit()
    conn.close()

@app.route('/track/<link_id>')
def track_ip(link_id):
    ip = request.remote_addr
    user_agent = request.headers.get('User-Agent')
    timestamp = datetime.utcnow().isoformat()

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    visit_id = str(uuid.uuid4())
    c.execute("INSERT INTO visits (id, ip, user_agent, timestamp) VALUES (?, ?, ?, ?)",
              (visit_id, ip, user_agent, timestamp))
    conn.commit()
    conn.close()

    return redirect("https://www.google.com")

@app.route('/api/visits')
def get_visits():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT ip, user_agent, timestamp FROM visits ORDER BY timestamp DESC")
    data = c.fetchall()
    conn.close()
    return jsonify([{"ip": x[0], "user_agent": x[1], "timestamp": x[2]} for x in data])

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
