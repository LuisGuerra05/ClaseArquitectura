'''
Este archivo implementa una API web para gestionar tareas usando Flask
'''

import json
import os
import sys
from datetime import datetime
from flask import Flask, jsonify, request, render_template, redirect, url_for
from collections import defaultdict

# ----------------------------
# Configuración inicial
# ----------------------------
TASKS_FILE = os.path.join(os.path.dirname(__file__), 'tasks.json')
app = Flask(__name__)

# ----------------------------
# Sistema de monitoreo de errores
# ----------------------------
error_stats = defaultdict(int)
error_log = []

def log_error(error_type, error_message, endpoint):
    """Registra errores para monitoreo"""
    error_stats[error_type] += 1
    error_entry = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'type': error_type,
        'message': error_message,
        'endpoint': endpoint
    }
    error_log.append(error_entry)
    print(f"🚨 ERROR DETECTADO: {error_type} en {endpoint} - {error_message}")

@app.route('/errors/stats')
def error_stats_view():
    """Devuelve estadísticas de errores recientes"""
    return jsonify({
        'total_errors': sum(error_stats.values()),
        'error_types': dict(error_stats),
        'recent_errors': error_log[-10:]
    })

# ----------------------------
# Logging de eventos (a consola o servicio externo)
# ----------------------------
def log_event(message):
    """Registra eventos importantes"""
    try:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_message = f"[{timestamp}] {message}"
        print(f"📝 LOG: {log_message}")
        with open("app_logs.txt", "a") as f:
            f.write(log_message + "\n")
    except Exception as e:
        log_error("500_INTERNAL_ERROR", f"Error en sistema de logging: {str(e)}", "log_event")

# ----------------------------
# Funciones de negocio
# ----------------------------
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
    port = request.host.split(':')[1]  # <--- Esto da el puerto como string
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

# ----------------------------
# API REST
# ----------------------------
@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    return jsonify(load_tasks())

@app.route('/api/tasks', methods=['POST'])
def add_task():
    data = request.json
    if not data:
        log_error("400_BAD_REQUEST", "JSON vacío o malformado", "/api/tasks")
        return jsonify({"error": "Se requiere JSON válido"}), 400

    if 'title' not in data or not data['title'].strip():
        log_error("400_BAD_REQUEST", "Título faltante o vacío", "/api/tasks")
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
    log_error("404_NOT_FOUND", f"Tarea con ID {task_id} no encontrada", "/api/tasks/complete")
    return jsonify({"error": "Tarea no encontrada"}), 404

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    tasks = load_tasks()
    if 0 <= task_id < len(tasks):
        deleted = tasks.pop(task_id)
        save_tasks(tasks)
        log_event(f"API: Tarea eliminada: {deleted['title']}")
        return jsonify(deleted)
    log_error("404_NOT_FOUND", f"Tarea con ID {task_id} no encontrada", "/api/tasks/delete")
    return jsonify({"error": "Tarea no encontrada"}), 404

@app.route('/api/tasks/simulate-error', methods=['POST'])
def simulate_error():
    try:
        result = 1 / 0
        return jsonify({"result": result})
    except ZeroDivisionError:
        log_error("500_INTERNAL_ERROR", "División por cero en simulación", "/api/tasks/simulate-error")
        return jsonify({"error": "Error interno del servidor - División por cero"}), 500
    except Exception as e:
        log_error("500_INTERNAL_ERROR", f"Error inesperado: {str(e)}", "/api/tasks/simulate-error")
        return jsonify({"error": "Error interno del servidor"}), 500

# ----------------------------
# Rutas Web
# ----------------------------
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
# Main
# ----------------------------
if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
    print(f"Servidor iniciado en puerto: {port}")
    app.run(host='0.0.0.0', port=port, debug=True)
