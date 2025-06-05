import requests

base_url = "http://localhost:8080"

print("Iniciando pruebas de errores...\n")

# Error 400: POST sin 'title'
r1 = requests.post(f"{base_url}/api/tasks", json={})
print("400 response:", r1.status_code)

# Error 404: tarea inexistente
r2 = requests.delete(f"{base_url}/api/tasks/999")
print("404 response:", r2.status_code)

# Error 500: división por cero
r3 = requests.get(f"{base_url}/error500")
print("500 response:", r3.status_code)
