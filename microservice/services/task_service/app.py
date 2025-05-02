from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

STORAGE_URL = "http://localhost:5002/storage/tasks"
LOGGING_URL = "http://localhost:5003/log"

# Utils
def log_event(message):
    try:
        requests.post(LOGGING_URL, json={"message": message})
    except:
        pass  # Ignora errores si logging_service no está activo

def load_tasks():
    response = requests.get(STORAGE_URL)
    return response.json() if response.status_code == 200 else []

def save_tasks(tasks):
    requests.post(STORAGE_URL, json=tasks)

@app.route("/", methods=["GET"])
def home():
    return "🧠 Task Service activo", 200

@app.route("/tasks", methods=["GET"])
def get_tasks():
    tasks = load_tasks()
    return jsonify(tasks)

@app.route("/tasks", methods=["POST"])
def add_task():
    data = request.get_json()
    title = data.get("title")
    description = data.get("description", "")

    if not title:
        return jsonify({"error": "Falta el título"}), 400

    tasks = load_tasks()
    new_task = {
        "id": len(tasks) + 1,
        "title": title,
        "description": description,
        "completed": False
    }
    tasks.append(new_task)
    save_tasks(tasks)
    log_event(f"Tarea agregada: {title}")

    return jsonify(new_task), 201

@app.route("/tasks/<int:task_id>/complete", methods=["PUT"])
def complete_task(task_id):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = True
            save_tasks(tasks)
            log_event(f"Tarea completada: {task['title']}")
            return jsonify(task), 200

    return jsonify({"error": "Tarea no encontrada"}), 404

@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    tasks = load_tasks()
    updated_tasks = [t for t in tasks if t["id"] != task_id]

    if len(tasks) == len(updated_tasks):
        return jsonify({"error": "Tarea no encontrada"}), 404

    save_tasks(updated_tasks)
    log_event(f"Tarea eliminada con ID: {task_id}")
    return jsonify({"status": "success"}), 200

if __name__ == "__main__":
    app.run(port=5001)
