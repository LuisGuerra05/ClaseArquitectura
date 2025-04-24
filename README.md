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
