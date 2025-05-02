class TaskView:
    def show_menu(self):
        print("\n📋 Menú de opciones:")
        print("1. Agregar tarea")
        print("2. Listar tareas")
        print("3. Marcar tarea como completada")
        print("4. Eliminar tarea")
        print("5. Salir")

    def get_input(self, prompt):
        return input(prompt)

    def show_tasks(self, tasks):
        if not tasks:
            print("No hay tareas.")
            return
        print("\nLista de tareas:")
        for i, task in enumerate(tasks, start=1):
            status = "✅" if task.completed else "❌"
            print(f"{i}. [{status}] {task.title} - {task.description}")

    def show_message(self, message):
        print(message)