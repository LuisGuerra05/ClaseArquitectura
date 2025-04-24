import json
import os

# ------------------------------
# Modelo: Tarea
# ------------------------------
class Task:
    def __init__(self, title: str, description: str, completed: bool = False):
        self.title = title
        self.description = description
        self.completed = completed

    # Convertir la tarea a diccionario para guardar en JSON
    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "completed": self.completed
        }

    # Crear una tarea a partir de un diccionario (desde JSON)
    @staticmethod
    def from_dict(data):
        return Task(data["title"], data["description"], data["completed"])

# ------------------------------
# Gestor de tareas: maneja lógica y almacenamiento
# ------------------------------
class TaskManager:
    def __init__(self, filepath="tasks.json"):
        self.filepath = filepath
        self.tasks = self.load_tasks()  # Cargar tareas desde archivo al iniciar

    def load_tasks(self):
        if os.path.exists(self.filepath):
            with open(self.filepath, "r") as f:
                return [Task.from_dict(t) for t in json.load(f)]
        return []

    def save_tasks(self):
        with open(self.filepath, "w") as f:
            json.dump([t.to_dict() for t in self.tasks], f, indent=4)

    def add_task(self, title, description):
        task = Task(title, description)
        self.tasks.append(task)
        self.save_tasks()  # Guardar cada vez que se agrega una tarea
        print("✅ Tarea agregada.")

    def list_tasks(self):
        if not self.tasks:
            print("No hay tareas.")
            return
        print("\nLista de tareas:")
        for i, task in enumerate(self.tasks, start=1):
            status = "✅" if task.completed else "❌"
            print(f"{i}. [{status}] {task.title} - {task.description}")

    def complete_task(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index].completed = True
            self.save_tasks()  # Guardar cada vez que se completa una tarea
            print("Tarea marcada como completada.")
        else:
            print("❌ Índice inválido.")

    def delete_task(self, index):
        if 0 <= index < len(self.tasks):
            removed = self.tasks.pop(index)
            self.save_tasks()  # Guardar cada vez que se elimina una tarea
            print(f"Tarea '{removed.title}' eliminada.")
        else:
            print("❌ Índice inválido.")

# ------------------------------
# Aplicación CLI: interacción con el usuario
# ------------------------------
class App:
    def __init__(self):
        self.manager = TaskManager()

    def show_menu(self):
        print("\n📋 Menú de opciones:")
        print("1. Agregar tarea")
        print("2. Listar tareas")
        print("3. Marcar tarea como completada")
        print("4. Eliminar tarea")
        print("5. Salir")

    def run(self):
        while True:
            self.show_menu()
            choice = input("Selecciona una opción: ")
            if choice == "1":
                title = input("Título: ")
                description = input("Descripción: ")
                self.manager.add_task(title, description)
            elif choice == "2":
                self.manager.list_tasks()
            elif choice == "3":
                try:
                    idx = int(input("Número de tarea: ")) - 1
                    self.manager.complete_task(idx)
                except ValueError:
                    print("❌ Entrada inválida.")
            elif choice == "4":
                try:
                    idx = int(input("Número de tarea: ")) - 1
                    self.manager.delete_task(idx)
                except ValueError:
                    print("❌ Entrada inválida.")
            elif choice == "5":
                print("👋 ¡Hasta luego!")
                break
            else:
                print("❌ Opción inválida.")

# ------------------------------
# Punto de entrada de la aplicación
# ------------------------------
if __name__ == "__main__":
    app = App()
    app.run()