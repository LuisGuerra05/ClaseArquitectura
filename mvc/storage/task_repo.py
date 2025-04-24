import json
import os
from models.task import Task

# Clase encargada de la persistencia de datos en archivo JSON
class TaskRepo:
    def __init__(self, filepath=None):
        # Si no se especifica ruta, guardar el JSON en la misma carpeta del archivo actual
        if filepath is None:
            self.filepath = os.path.join(os.path.dirname(__file__), "task.json")
        else:
            self.filepath = filepath

    # Cargar tareas desde el archivo JSON
    def load_tasks(self):
        if os.path.exists(self.filepath):
            with open(self.filepath, "r") as f:
                return [Task.from_dict(t) for t in json.load(f)]
        return []

    # Guardar tareas en el archivo JSON
    def save_tasks(self, tasks):
        with open(self.filepath, "w") as f:
            json.dump([t.to_dict() for t in tasks], f, indent=4)