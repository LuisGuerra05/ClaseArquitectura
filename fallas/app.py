'''
Este archivo implementa una API web para gestionar tareas usando Flask
'''

import json
import os
import sys
import requests
from datetime import datetime
from collections import defaultdict, deque
from flask import Flask, jsonify, request, render_template, redirect, url_for

# Ruta del archivo de tareas
TASKS_FILE = os.path.join(os.path.dirname(__file__), 'tasks.json')

app = Flask(__name__)

# ----------------------------
# Sistema de monitoreo de errores
# ----------------------------
error_stats = defaultdict(int)
error_log = deque(maxlen=100)

@app.errorhandler(400)
def bad_request(e):
    error_stats['400_BAD_REQUEST'] += 1
    error_log.append(f"400 - BAD REQUEST - {request.path}")
    return jsonify({"error": "Solicitud inválida"}), 400

@app.errorhandler(404)
def not_found(e):
    error_stats['404_NOT_FOUND'] += 1
    error_log.append(f"404 - NOT FOUND - {request.path}")
    return jsonify({"error": "Recurso no encontrado"}), 404

@app.errorhandler(500)
def internal_error(e):
    error_stats['500_INTERNAL_ERROR'] += 1
    error_log.append(f"500 - INTERNAL SERVER ERROR - {request.path}")
    return jsonify({"error": "Error interno del servidor"}), 500

@app.route('/errors/stats')
def error_stats_view():
    return jsonify({
        'total_errors': sum(error_stats.values()),
        'error_types': dict(error_stats),
        'recent_errors': list(error_log)[-10:]
    })

@app.route('/error500')
def trigger_error():
    return 1 / 0  # Para probar error 500

# ----------------------------
# Funciones de negocio
# ----------------------------

def log_event(message):
    try:
        requests.post("http://localhost:5003/log", json={"message": message}, timeout=1)
    except:
        pass

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, "r") as file:
        try:
            tasks = json.load(file)
            return [
                {**task, "completed": task.get("completed", False)}
                for task in tasks if isinstance(task, dict) and 'title' in task
            ]
        except json.JSONDecodeError:
            return []

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent=4)

# ----------------------------
# Rutas principales
# ----------------------------

@app.route('/')
def index():
    tasks = load_tasks()
    port = request.host.split(':')[1]
    return render_template('index.html', tasks=tasks, port=port)

@app.route('/info')
def server_info():
    return jsonify({
        'server_port': request.host.split(':')[1],
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok"}), 200

# API REST

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    return jsonify(load_tasks())

@app.route('/api/tasks', methods=['POST'])
def add_task():
    data = request.json
    if not data or 'title' not in data:
        return jsonify({"error": "El título de la tarea es requerido"}), 400
    tasks = load_tasks()
    new_task = {'title': data['title'], 'completed': False}
    tasks.append(new_task)
    save_tasks(tasks)
    log_event(f"API: Nueva tarea añadida: {data['title']}")
    return jsonify(new_task), 201

@app.route('/api/tasks/<int:task_id>/complete', methods=['PUT'])
def complete_task(task_id):
    tasks = load_tasks()
    if 0 <= task_id < len(tasks):
        tasks[task_id]['completed'] = True
        save_tasks(tasks)
        log_event(f"API: Tarea completada: {tasks[task_id]['title']}")
        return jsonify(tasks[task_id])
    return jsonify({"error": "Tarea no encontrada"}), 404

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    tasks = load_tasks()
    if 0 <= task_id < len(tasks):
        deleted = tasks.pop(task_id)
        save_tasks(tasks)
        log_event(f"API: Tarea eliminada: {deleted['title']}")
        return jsonify(deleted)
    return jsonify({"error": "Tarea no encontrada"}), 404

# Web UI

@app.route('/tasks/add', methods=['POST'])
def web_add_task():
    title = request.form.get('title')
    if title:
        tasks = load_tasks()
        tasks.append({'title': title, 'completed': False})
        save_tasks(tasks)
        log_event(f"WEB: Nueva tarea añadida: {title} (servidor {request.host})")
    return redirect(url_for('index'))

@app.route('/tasks/<int:task_id>/complete', methods=['POST'])
def web_complete_task(task_id):
    tasks = load_tasks()
    if 0 <= task_id < len(tasks):
        tasks[task_id]['completed'] = True
        save_tasks(tasks)
        log_event(f"WEB: Tarea completada: {tasks[task_id]['title']} (servidor {request.host})")
    return redirect(url_for('index'))

@app.route('/tasks/<int:task_id>/delete', methods=['POST'])
def web_delete_task(task_id):
    tasks = load_tasks()
    if 0 <= task_id < len(tasks):
        title = tasks[task_id]['title']
        tasks.pop(task_id)
        save_tasks(tasks)
        log_event(f"WEB: Tarea eliminada: {title} (servidor {request.host})")
    return redirect(url_for('index'))

# ----------------------------

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
    print(f"Servidor iniciado en puerto: {port}")
    app.run(host='0.0.0.0', port=port, debug=True)
