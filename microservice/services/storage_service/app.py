from flask import Flask, request, jsonify
import os
import json

app = Flask(__name__)
TASKS_FILE = "tasks.json"

@app.route("/", methods=["GET"])
def home():
    return "💾 Storage Service activo", 200

@app.route("/storage/tasks", methods=["GET"])
def get_tasks():
    if not os.path.exists(TASKS_FILE):
        return jsonify([]), 200

    with open(TASKS_FILE, "r") as f:
        tasks = json.load(f)

    return jsonify(tasks), 200

@app.route("/storage/tasks", methods=["POST"])
def save_tasks():
    tasks = request.get_json()

    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

    return jsonify({"status": "success", "message": "Tareas guardadas"}), 201

if __name__ == "__main__":
    app.run(port=5002)
