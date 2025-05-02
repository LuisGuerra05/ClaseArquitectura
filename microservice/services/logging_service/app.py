from flask import Flask, request, jsonify
from datetime import datetime
import os

app = Flask(__name__)
LOG_FILE = "log.txt"

@app.route("/", methods=["GET"])
def home():
    return "📝 Logging Service funcionando", 200

@app.route("/log", methods=["POST"])
def log_event():
    data = request.get_json()
    message = data.get("message", "Sin mensaje")
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    log_entry = f"{timestamp} {message}\n"

    with open(LOG_FILE, "a") as f:
        f.write(log_entry)

    return jsonify({"status": "success", "message": "Evento registrado"}), 201

@app.route("/logs", methods=["GET"])
def get_logs():
    if not os.path.exists(LOG_FILE):
        return jsonify([])

    with open(LOG_FILE, "r") as f:
        lines = f.readlines()

    return jsonify([line.strip() for line in lines])

if __name__ == "__main__":
    app.run(port=5003)
