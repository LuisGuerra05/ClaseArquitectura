from flask import Flask, request, redirect, render_template_string
import requests

app = Flask(__name__)
TASK_SERVICE_URL = "http://localhost:5001"

TEMPLATE = """
<!doctype html>
<html>
<head>
    <title>Gestor de Tareas</title>
</head>
<body>
    <h1>📋 Lista de Tareas</h1>

    <form method="POST" action="/tasks">
        <input type="text" name="title" placeholder="Título" required>
        <input type="text" name="description" placeholder="Descripción">
        <button type="submit">Agregar</button>
    </form>

    <ul>
        {% for task in tasks %}
            <li>
                {% if task.completed %}
                    ✅ <del>{{ task.title }} - {{ task.description }}</del>
                {% else %}
                    ❌ {{ task.title }} - {{ task.description }}
                    <form method="POST" action="/tasks/{{ task.id }}/complete" style="display:inline">
                        <button type="submit">Completar</button>
                    </form>
                {% endif %}
                <form method="POST" action="/tasks/{{ task.id }}/delete" style="display:inline">
                    <button type="submit">Eliminar</button>
                </form>
            </li>
        {% endfor %}
    </ul>
</body>
</html>
"""

@app.route("/", methods=["GET"])
def home():
    response = requests.get(f"{TASK_SERVICE_URL}/tasks")
    tasks = response.json() if response.ok else []
    return render_template_string(TEMPLATE, tasks=tasks)

@app.route("/tasks", methods=["POST"])
def add_task():
    title = request.form.get("title")
    description = request.form.get("description", "")
    requests.post(f"{TASK_SERVICE_URL}/tasks", json={
        "title": title,
        "description": description
    })
    return redirect("/")

@app.route("/tasks/<int:task_id>/complete", methods=["POST"])
def complete_task(task_id):
    requests.put(f"{TASK_SERVICE_URL}/tasks/{task_id}/complete")
    return redirect("/")

@app.route("/tasks/<int:task_id>/delete", methods=["POST"])
def delete_task(task_id):
    requests.delete(f"{TASK_SERVICE_URL}/tasks/{task_id}")
    return redirect("/")

if __name__ == "__main__":
    app.run(port=5000)
