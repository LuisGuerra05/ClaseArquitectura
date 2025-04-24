from models.task import Task
from storage.task_repo import TaskRepo
from views.task_view import TaskView

# Clase encargada de coordinar el flujo entre vista, modelo y almacenamiento
class TaskController:
    def __init__(self):
        self.repo = TaskRepo()
        self.view = TaskView()
        self.tasks = self.repo.load_tasks()  # Cargar tareas al iniciar

    # Ciclo principal de la aplicación
    def run(self):
        while True:
            self.view.show_menu()
            choice = self.view.get_input("Selecciona una opción: ")

            if choice == "1":  # Agregar tarea
                title = self.view.get_input("Título: ")
                description = self.view.get_input("Descripción: ")
                self.tasks.append(Task(title, description))
                self.repo.save_tasks(self.tasks)  # Guardar después de agregar
                self.view.show_message("✅ Tarea agregada.")

            elif choice == "2":  # Listar tareas
                self.view.show_tasks(self.tasks)

            elif choice == "3":  # Marcar como completada
                try:
                    idx = int(self.view.get_input("Número de tarea: ")) - 1
                    if 0 <= idx < len(self.tasks):
                        self.tasks[idx].completed = True
                        self.repo.save_tasks(self.tasks)  # Guardar después de completar
                        self.view.show_message("Tarea marcada como completada.")
                    else:
                        self.view.show_message("❌ Índice inválido.")
                except ValueError:
                    self.view.show_message("❌ Entrada inválida.")

            elif choice == "4":  # Eliminar tarea
                try:
                    idx = int(self.view.get_input("Número de tarea: ")) - 1
                    if 0 <= idx < len(self.tasks):
                        removed = self.tasks.pop(idx)
                        self.repo.save_tasks(self.tasks)  # Guardar después de eliminar
                        self.view.show_message(f"Tarea '{removed.title}' eliminada.")
                    else:
                        self.view.show_message("❌ Índice inválido.")
                except ValueError:
                    self.view.show_message("❌ Entrada inválida.")

            elif choice == "5":  # Salir
                self.view.show_message("👋 ¡Hasta luego!")
                break

            else:
                self.view.show_message("❌ Opción inválida.")
