# Gestión de Tareas - Diferentes Enfoques de Arquitectura

Este proyecto muestra cómo desarrollar una aplicación para gestionar tareas personales usando tres enfoques arquitectónicos distintos:

1. **Monolítico**: Un único archivo que maneja toda la lógica, presentación y persistencia.
2. **MVC (Modelo-Vista-Controlador)**: Separación clara de responsabilidades entre el modelo de datos, la lógica de negocio y la vista.
3. **Microservicio**: Dividir la aplicación en servicios independientes que se comunican entre sí.

---

## Descripción General

La aplicación permite a los usuarios gestionar tareas personales mediante un sistema de consola, donde pueden:
- **Agregar tareas**
- **Listar tareas**
- **Marcar tareas como completadas**
- **Eliminar tareas**

Cada enfoque utiliza el mismo flujo básico, pero con una estructura diferente para mostrar cómo se pueden manejar los mismos requisitos de diferentes maneras.

---

## Enfoque 1: Monolítico

En este enfoque, toda la lógica de la aplicación (gestión de tareas, interfaz de usuario, persistencia de datos) se maneja en un único archivo `main.py`. Este es un enfoque más simple, pero a medida que la aplicación crece, puede volverse difícil de mantener.

**Características:**
- Todo el código en un solo archivo.
- Fácil de entender y prototipar.
- Ideal para pequeñas aplicaciones, pero menos escalable.

**Estructura:**
```
monolitic/
│
├── main.py                # Punto de entrada que ejecuta la app   
│     
└── task.json              # Para almacenar las tareas
```

---
## Enfoque 2: MVC (Modelo-Vista-Controlador)

El patrón **MVC** se utiliza para separar la lógica de la aplicación en tres componentes:
- **Modelo**: Define la estructura de los datos (tareas).
- **Vista**: Se encarga de la interfaz de usuario (consola).
- **Controlador**: Maneja la lógica de negocio y las interacciones entre modelo y vista.

### Características:
- **Modelo** para representar tareas.
- **Vista** para mostrar la interfaz de usuario.
- **Controlador** para gestionar la lógica de negocio.
- Modular, escalable y fácil de mantener.

### Estructura:
```
mvc/
│
├── controllers/        
│   └── task_controller.py # Gestiona la lógica de negocio
│
├── models/        
│   └── task.py            # Define la clase de la tarea
│
├── views/            
│   └── task_view.py       # Muestra la interfaz de usuario
│
├── storage/        
│   └── task_repo.py       # Gestiona la persistencia de datos
│   └── task.json          # Almacena las tareas
│
├── assets/                 
│   └── logo.png
│
├── main.py                # Punto de entrada que ejecuta la app
├── requirements.txt        
└── README.md   
```

---

## Enfoque 3: Microservicios

En este enfoque, la aplicación se divide en **varios servicios independientes**, cada uno responsable de una función específica (gestión, almacenamiento, registro, interfaz). Estos servicios se comunican entre sí usando **peticiones HTTP** a través de Flask y `requests`.

### Características:
- Cada servicio corre de forma independiente en un puerto distinto.
- Separación total de responsabilidades (single responsibility).
- Escalable, mantenible y alineado con arquitecturas modernas.
- Ideal para despliegues distribuidos o contenerizados (ej. Docker).

### Microservicios:
| Servicio             | Función principal                                           | Puerto |
|----------------------|-------------------------------------------------------------|--------|
| **Client**           | Interfaz web (formulario + lista de tareas)                | 5000   |
| **Task Service**     | Lógica de negocio (crear, completar, eliminar tareas)      | 5001   |
| **Storage Service**  | Persistencia en `tasks.json`                               | 5002   |
| **Logging Service**  | Registro de eventos (log.txt)                              | 5003   |
| **Notification Service** | (Opcional) Notificaciones al completar tareas         | —      |

### Flujo:
```
Usuario → Client (5000) → Task Service (5001)
         ↘                     ↓
       Logging (5003) ← Storage (5002)
```

### Estructura:
```
microservice/
│
├── client/                    # Interfaz web que interactúa con el Task Service
│   └── app.py
│
├── services/
│   ├── logging_service/       # Registra acciones (crear, eliminar, completar)
│   │   └── app.py
│   │   └── log.txt
│
│   ├── storage_service/       # Gestiona el archivo tasks.json
│   │   └── app.py
│   │   └── tasks.json
│
│   ├── task_service/          # Lógica de negocio de las tareas
│   │   └── app.py
│
│   └── notification_service/  # (Opcional) Para notificaciones futuras
│       └── app.py
```

### ¿Cómo usarlo?

1. Abre 4 terminales y ejecuta:

```bash
# Terminal 1
cd services/task_service
python app.py

# Terminal 2
cd services/storage_service
python app.py

# Terminal 3
cd services/logging_service
python app.py

# Terminal 4
cd client
python app.py
```

2. Visita `http://localhost:5000` para interactuar visualmente.

3. Verifica `tasks.json` (almacenamiento) y `log.txt` (registro de eventos).
