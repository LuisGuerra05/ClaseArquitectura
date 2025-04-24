# Modelo de datos que representa una tarea individual
class Task:
    def __init__(self, title: str, description: str, completed: bool = False):
        self.title = title
        self.description = description
        self.completed = completed

    # Convertir la tarea a diccionario (para guardar en JSON)
    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "completed": self.completed
        }

    # Crear una tarea desde un diccionario (al leer JSON)
    @staticmethod
    def from_dict(data):
        return Task(data["title"], data["description"], data["completed"])
