![Logo](../mvc/assets/UAI.png)
# Arquitectura de Sistemas: TICS317

---
¡Bienvenidos al repositorio de Arquitectura!. Acá haremos algunos ejercicios complementarios a las clases para profundizar los aprendizajes




# ¿Que necesitamos?

| **Categoría**               | **Biblioteca**                                                                                                  | **Descripción**                                                              |
|----------------------------|------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------|
| **1. Lenguaje base**        | [![python](https://img.shields.io/badge/python-3.7+-blue)](https://www.python.org/downloads/)                   | Lenguaje principal del proyecto. Versión recomendada: 3.7 o superior.        |
| **2. Framework web**        | [![flask](https://img.shields.io/badge/flask-pip--install--flask-green)](https://pypi.org/project/Flask/)       | Microframework ligero para desarrollar los servicios web.                    |
| **3. Peticiones HTTP**      | [![requests](https://img.shields.io/badge/requests-pip--install--requests-green)](https://pypi.org/project/requests/) | Librería para hacer llamadas HTTP entre los microservicios.                  |

### El proyecto se desarrolla en:

* Enviroment de Python [![versions](https://img.shields.io/badge/python-3.13-white)](https://www.python.org/downloads/)

* Entorno de Desarrollo Integrado (IDE) [![versions](https://img.shields.io/badge/PyCharm-2024.3.4-white)](https://www.jetbrains.com/help/pycharm/installation-guide.html)


## 🎓 Caso de Estudio:  Microservice Task Manager

## Descripción del Proyecto

**Microservice Task Manager** es una aplicación basada en arquitectura de microservicios que permite gestionar tareas (crear, listar, completar y eliminar) a través de varios servicios independientes que se comunican entre sí. El proyecto está desarrollado con **Flask** y utiliza un enfoque de diseño basado en microservicios, donde cada servicio es responsable de una tarea específica y se comunica con los demás servicios a través de HTTP.

El sistema incluye varios microservicios que gestionan diferentes aspectos de la aplicación:

- **Client**: Interfaz del usuario que permite interactuar con los servicios de tareas y logs.
- **Logging Service**: Registra eventos importantes como agregar o completar tareas.
- **Storage Service**: Gestiona la lectura y escritura de tareas en un archivo JSON.
- **Task Service**: Maneja la lógica de negocio de las tareas (creación, eliminación y actualización de estado de las tareas).

## Caso de Estudio Simulado

Imagina que eres un gerente de proyectos en una pequeña empresa que está comenzando a gestionar tareas de equipo de forma más estructurada. Cada miembro del equipo tiene tareas asignadas, y tú necesitas un sistema para seguir el progreso de las tareas, asignar nuevas y asegurarte de que se completen a tiempo.

Este sistema, dividido en microservicios, permite gestionar las tareas de manera sencilla y efectiva. Los microservicios permiten que los diferentes componentes del sistema sean escalables y fáciles de mantener, lo que resulta en una solución eficiente para el manejo de tareas dentro de tu equipo.

### Flujo del Caso de Estudio

1. **Agregar tareas**: Como gerente de proyectos, accedes al sistema y creas nuevas tareas para el equipo a través de la interfaz del cliente.
2. **Listar tareas**: Puedes ver todas las tareas que se han agregado, indicando si están completas o no.
3. **Completar tareas**: Una vez que se haya trabajado en una tarea, puedes marcarla como completada.
4. **Eliminar tareas**: Si una tarea ya no es relevante, puedes eliminarla del sistema.
5. **Ver logs**: A través del sistema de logging, puedes revisar todas las acciones realizadas, como la creación o eliminación de tareas.

## Cómo Funciona

El sistema se divide en varios microservicios, que se ejecutan en diferentes puertos locales:

1. **Client** (Puerto 5000): Interfaz del usuario donde se puede interactuar con el sistema.
2. **Task Service** (Puerto 5001): Gestiona la creación, actualización y eliminación de tareas.
3. **Storage Service** (Puerto 5002): Se encarga de leer y escribir las tareas en un archivo `tasks.json`.
4. **Logging Service** (Puerto 5003): Registra los eventos y acciones realizadas, como agregar, completar o eliminar tareas.


## Estructura del proyecto

```

microservice/
│
├── client/
│   └── __init__.py
│   └── app.py
│
├── services/
│   ├── logging_service/
│   |   └── __init__.py
│   │   └── app.py
│   │   └── log.txt (se crea automáticamente)
│
│   ├── notification_service/ (Opcional) 
│   |   └── __init__.py
│   │   └── app.py
│
│   ├── storage_service/
│   |   └── __init__.py
│   │   └── app.py
|   |   └── tasks.json (storage.json)
│
│   └── task_service/
│   |   └── __init__.py
│   |   └── app.py
│   |   └── tasks.json

```
---
Cada servicio debe iniciarse manualmente en una terminal distinta. Por ejemplo:

```
# En una terminal
cd services/task_service
python app.py

# En otra
cd services/logging_service
python app.py
```

---
### logging_service/app.py

Servicio para registrar eventos en un archivo log.txt. Expone:

- GET / - Página de bienvenida
- POST /log - Recibe un mensaje JSON y lo guarda en el log
- GET /logs - Devuelve todos los logs registrados


### notification_service/app.py
Pendiente de implementación. Posibles ideas:
- POST /notify para enviar una notificación
- GET /status para ver estado del servicio

### storage_service/app.py

Lee y guarda tareas en un archivo tasks.json. Expone:
- GET /storage/tasks - Devuelve las tareas guardadas
- POST /storage/tasks - Guarda una nueva lista de tareas
- GET / - Página de bienvenida

### task_service/app.py

Maneja la lógica de las tareas. Expone:
- GET /tasks - Lista todas las tareas
- POST /tasks - Crea una nueva tarea
- PUT /tasks/<id>/complete - Marca una tarea como completada
- DELETE /tasks/<id> - Elimina una tarea
- GET / - Página de bienvenida

### task_service/tasks.json

Archivo persistente con las tareas registradas


### Tabla resumen de puertos

| Servicio           | Descripción                              | Puerto |
|--------------------|------------------------------------------|--------|
| Client             | Interfaz de usuario                      | 5000   |
| Task Service       | Gestión de lógica de tareas              | 5001   |
| Storage Service    | Lectura/escritura de tareas en JSON      | 5002   |
| Logging Service    | Registro de eventos                      | 5003   |
| Notification (WIP) | Envío de notificaciones (a futuro)       | -      |


### Futuras Mejoras

- Implementar notification_service
- Conexión entre servicios usando llamadas HTTP
- Mejorar manejo de errores y validaciones
- Contenerización con Docker
- Agregar autenticación simple
- Registrar eventos automáticamente en logging_service desde task_service

