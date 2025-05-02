from models.task import Task
from storage.task_repo import TaskRepo
from views.task_view import TaskView

class TaskController:
    def __init__(self):
        self.repo = TaskRepo()
        self.view = TaskView()
        self.tasks = self.repo.load_tasks()

    def run(self):
        while True:
            self.view.show_menu()
            choice = self.view.get_input("Selecciona una opción: ")

            if choice == "1":
                self.add_task()
            elif choice == "2":
                self.list_tasks()
            elif choice == "3":
                self.complete_task()
            elif choice == "4":
                self.remove_task()
            elif choice == "5":
                self.view.show_message("👋 ¡Hasta luego!")
                break
            else:
                self.view.show_message("❌ Opción inválida.")

    def add_task(self):
        title = self.view.get_input("Título: ")
        description = self.view.get_input("Descripción: ")
        self.tasks.append(Task(title, description))
        self.repo.save_tasks(self.tasks)
        self.view.show_message("✅ Tarea agregada.")

    def list_tasks(self):
        self.view.show_tasks(self.tasks)

    def complete_task(self):
        try:
            idx = int(self.view.get_input("Número de tarea: ")) - 1
            if 0 <= idx < len(self.tasks):
                self.tasks[idx].mark_done()
                self.repo.save_tasks(self.tasks)
                self.view.show_message("Tarea marcada como completada.")
            else:
                self.view.show_message("❌ Índice inválido.")
        except ValueError:
            self.view.show_message("❌ Entrada inválida.")

    def remove_task(self):
        try:
            idx = int(self.view.get_input("Número de tarea: ")) - 1
            if 0 <= idx < len(self.tasks):
                removed = self.tasks.pop(idx)
                self.repo.save_tasks(self.tasks)
                self.view.show_message(f"Tarea '{removed.title}' eliminada.")
            else:
                self.view.show_message("❌ Índice inválido.")
        except ValueError:
            self.view.show_message("❌ Entrada inválida.")