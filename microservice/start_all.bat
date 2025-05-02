@echo off
echo Iniciando todos los microservicios...

start cmd /k "cd services\storage_service && python app.py"
start cmd /k "cd services\logging_service && python app.py"
start cmd /k "cd services\task_service && python app.py"
start cmd /k "cd client && python app.py"

echo Todos los servicios han sido lanzados en terminales separadas.
pause