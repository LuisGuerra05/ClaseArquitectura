# Arquitectura de Sistemas: TICS317

---
¡Bienvenidos al repositorio de Arquitectura!. Acá haremos algunos ejercicios complementarios a las clases para profundizar los aprendizajes



# ¿Que necesitamos?
| **Categoría**              | **Biblioteca**                                                                                          | **Descripción**                                                        |
|----------------------------|----------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------|
| **1. Manejo de archivos**  | [![json](https://img.shields.io/badge/json-estándar-yellow)](https://docs.python.org/3/library/json.html) | Lectura y escritura de archivos `.json` para almacenar las tareas.     |
| **2. Sistema de archivos** | [![os](https://img.shields.io/badge/os-estándar-yellow)](https://docs.python.org/3/library/os.html)       | Interacción con el sistema de archivos para manejar rutas y archivos. |
| **3. Fecha y hora**        | [![datetime](https://img.shields.io/badge/datetime-estándar-yellow)](https://docs.python.org/3/library/datetime.html) | Registro de timestamps en logs y respuestas del servidor.   |
| **4. Framework web**       | [![flask](https://img.shields.io/badge/flask-pip--install--flask-green)](https://pypi.org/project/Flask/)       | Microframework ligero para desarrollar los servicios web.             |
| **5. Peticiones HTTP**     | [![requests](https://img.shields.io/badge/requests-pip--install--requests-green)](https://pypi.org/project/requests/) | Librería para hacer llamadas HTTP entre los microservicios.          |
| **6. Random**              | [![random](https://img.shields.io/badge/random-estándar-yellow)](https://docs.python.org/3/library/random.html) | Selección aleatoria de servidores en el balanceador de carga.         |
| **7. Sys**                 | [![sys](https://img.shields.io/badge/sys-estándar-yellow)](https://docs.python.org/3/library/sys.html) | Acceso a argumentos de línea de comandos para especificar puertos.     |
| **8. Templates web**       | [![jinja2](https://img.shields.io/badge/jinja2-incluido--con--flask-green)](https://jinja.palletsprojects.com/) | Motor de plantillas para generar HTML dinámico en Flask.              |

### El proyecto se desarrolla en:

* Enviroment de Python [![versions](https://img.shields.io/badge/python-3.13-white)](https://www.python.org/downloads/)

* Entorno de Desarrollo Integrado (IDE) [![versions](https://img.shields.io/badge/PyCharm-2024.3.4-white)](https://www.jetbrains.com/help/pycharm/installation-guide.html)

---
# Guía del Sistema de Gestión de Tareas con Balanceo de Cargas

## Introducción

Este documento explica paso a paso cómo funciona nuestro sistema de gestión de tareas. El sistema utiliza un diseño con múltiples servidores y un balanceador de cargas para distribuir el trabajo, similar a cómo funcionan las aplicaciones web de gran escala.

El balanceador de carga es un componente arquitectónico crucial que actúa como un "director de orquesta" inteligente, gestionando el tráfico y garantizando la robustez del sistema. No solo distribuye solicitudes, sino que también proporciona monitoreo, tolerancia a fallos y transparencia para los usuarios finales.
En arquitectura de sistemas, el balanceador representa uno de los componentes fundamentales para construir sistemas distribuidos altamente disponibles y escalables, permitiendo que aplicaciones complejas funcionen de manera confiable incluso cuando algunos componentes individuales fallan


## Índice

1. [Componentes del Sistema](#componentes-del-sistema)
2. [Funcionamiento Básico](#funcionamiento-básico)
3. [Configuración Paso a Paso](#configuración-paso-a-paso)
4. [Explicación Detallada de los Componentes](#explicación-detallada-de-los-componentes)
5. [Pruebas y Experimentación](#pruebas-y-experimentación)

## Componentes del Sistema

Nuestro sistema consta de varios archivos, cada uno con un propósito específico:

- **app.py**: La aplicación principal que maneja las tareas.
- **load_balancer.py**: Distribuye las solicitudes entre múltiples instancias de la aplicación.
- **index.html**: La interfaz de usuario que verás en tu navegador.
- **tasks.json**: Almacena todas las tareas creadas por los usuarios.

## Funcionamiento Básico

Imagina que eres el gerente de una oficina de correos con dos ventanillas (servidores) y una fila única de clientes. El balanceador de cargas es como el organizador que dirige a cada cliente a una ventanilla disponible. Así es como funciona nuestro sistema:

1. **El usuario hace una solicitud** a través del balanceador (puerto 8080).
2. **El balanceador elige** uno de los servidores disponibles (puerto 5001 o 5002).
3. **El servidor elegido procesa** la solicitud (muestra tareas, agrega una nueva, etc.).
4. **El servidor devuelve** el resultado al usuario a través del balanceador.

## Configuración Paso a Paso

### Paso 0: Preparación

Asegúrate de tener instalado Python y Flask. Puedes instalar Flask con:


> ```shell
> pip install flask requests
> ```


### Paso 1: Crear la Estructura de Archivos

Crea una carpeta para el proyecto y dentro de ella:

1. Crea un archivo `app.py` con el código proporcionado.
2. Crea un archivo `load_balancer.py` con el código proporcionado.
3. Crea una carpeta `templates` y dentro un archivo `index.html`.
4. El archivo `tasks.json` se creará automáticamente al iniciar el sistema.

### Paso 2: Iniciar los Servidores

Abre tres terminales diferentes:

**Terminal 1 - Primer servidor (Puerto 5001):**


> ```shell
> python app.py 5001
> ```


**Terminal 2 - Segundo servidor (Puerto 5002):**

> ```shell
> python app.py 5002
> ```


**Terminal 3 - Balanceador de cargas (Puerto 8080):**

> ```shell
> python load_balancer.py
> ```


### Paso 3: Acceder al Sistema

Abre tu navegador y visita:
- http://localhost:8080 (a través del balanceador)
- http://localhost:5001 (directamente al primer servidor)
- http://localhost:5002 (directamente al segundo servidor)

## Explicación Detallada de los Componentes

### app.py - El Corazón del Sistema

El archivo `app.py` es como el empleado de la oficina de correos. Este archivo:

1. **Crea y gestiona una aplicación web** usando Flask.
2. **Define funciones para manejar tareas**:
   - Cargar tareas desde `tasks.json`
   - Guardar tareas en `tasks.json`
   - Mostrar la lista de tareas
   - Agregar nuevas tareas
   - Marcar tareas como completadas
   - Eliminar tareas
3. **Configura rutas web** que el navegador puede visitar:
   - `/` - Muestra la página principal con todas las tareas
   - `/tasks/add` - Agrega una nueva tarea
   - `/tasks/{id}/complete` - Marca una tarea como completada
   - `/tasks/{id}/delete` - Elimina una tarea
4. **Inicia un servidor web** en el puerto especificado (5001 o 5002).

Cuando ejecutas `python app.py 5001`, estás iniciando un servidor que escucha en el puerto 5001 de tu computadora.

### load_balancer.py - El Director de Tráfico

El archivo `load_balancer.py` funciona como el organizador que dirige a los clientes. Este archivo:

1. **Crea un servidor web** que escucha en el puerto 8080.
2. **Mantiene una lista de servidores disponibles** (5001 y 5002).
3. **Cuando recibe una solicitud**:
   - Elige aleatoriamente uno de los servidores
   - Reenvía la solicitud exactamente como la recibió
   - Espera la respuesta del servidor elegido
   - Devuelve esa respuesta al usuario
4. **No modifica las respuestas** excepto para ajustar algunos encabezados técnicos.

Este diseño permite distribuir el trabajo entre múltiples servidores sin que el usuario tenga que saber cuál está usando.

### index.html - La Interfaz de Usuario

El archivo `index.html` es lo que el usuario ve en su navegador. Este archivo:

1. **Muestra un formulario** para agregar nuevas tareas.
2. **Lista todas las tareas existentes** con opciones para completarlas o eliminarlas.
3. **Muestra información sobre el servidor** que está atendiendo la solicitud actual.
4. **Tiene diferentes colores de fondo** dependiendo del servidor (azul para 5001, rosa para 5002).

La línea al final que dice "Servidor atendiendo esta solicitud: Puerto XXXX" te ayuda a ver qué servidor está procesando tu solicitud.

### tasks.json - El Almacén de Datos

El archivo `tasks.json` es como una carpeta de archivos compartida entre las ventanillas. Este archivo:

1. **Almacena todas las tareas** en formato JSON.
2. **Es leído y modificado** por ambos servidores.
3. **Persiste los datos** incluso cuando los servidores se reinician.

## Los Puertos y Su Significado

Imagina que los puertos son como números de teléfono para diferentes servicios en tu computadora:

- **Puerto 5001**: Primera instancia (copia) de tu aplicación de tareas.
- **Puerto 5002**: Segunda instancia (copia) de tu aplicación de tareas.
- **Puerto 8080**: El balanceador de cargas que distribuye el trabajo.

Cuando visitas:
- **localhost:5001**: Estás llamando directamente a la primera instancia.
- **localhost:5002**: Estás llamando directamente a la segunda instancia.
- **localhost:8080**: Estás llamando al balanceador, que te conectará con 5001 o 5002.

## Pruebas y Experimentación

Aquí hay algunas pruebas que puedes hacer para entender mejor el sistema:

1. **Agregar tareas a través del balanceador**:
   - Visita http://localhost:8080
   - Agrega varias tareas
   - Observa cómo el color de fondo cambia, indicando que estás siendo atendido por diferentes servidores

2. **Probar la tolerancia a fallos**:
   - Detén uno de los servidores (Ctrl+C en su terminal)
   - Sigue usando el sistema a través del balanceador
   - Observa que sigue funcionando, pero siempre con el mismo color de fondo

3. **Reiniciar un servidor caído**:
   - Vuelve a iniciar el servidor que detuviste
   - Continúa usando el sistema
   - Observa que el balanceador vuelve a distribuir las solicitudes entre ambos servidores

## Algunas consideraciones sobre balanceadores

### Importancia en Arquitecturas Modernas
El balanceador de carga es fundamental en:
1. **Escalabilidad horizontal**: Permite añadir más servidores para manejar más tráfico sin cambiar la aplicación
2. **Arquitecturas de microservicios**: Facilita la comunicación entre múltiples servicios independientes
3. **Alta disponibilidad**: Garantiza que el sistema siga funcionando incluso si algunos componentes fallan
4. **Despliegues sin tiempo de inactividad**: Permite actualizar servidores de forma gradual sin interrumpir el servicio

### Algoritmos de Distribución de Carga
Aunque tu implementación usa selección aleatoria, existen varios algoritmos comunes:
1. **Round Robin**: Distribuye solicitudes secuencialmente entre los servidores
2. **Menor número de conexiones**: Envía solicitudes al servidor con menos conexiones activas
3. **Tiempo de respuesta**: Selecciona el servidor con mejor tiempo de respuesta
4. **Hash IP**: Envía todas las solicitudes de una misma IP al mismo servidor
5. **Aleatorio**: Como en nuestra implementación, selecciona un servidor al azar


## Conclusión

Este sistema demuestra conceptos importantes utilizados en aplicaciones web de gran escala:

1. **Balanceo de cargas**: Distribuir el trabajo entre múltiples servidores.
2. **Alta disponibilidad**: Seguir funcionando incluso si un servidor falla.
3. **Escalabilidad horizontal**: Poder agregar más servidores para manejar más usuarios.

Aunque este ejemplo se ejecuta en una sola computadora, los mismos principios se aplican a sistemas con servidores distribuidos en diferentes máquinas o incluso en diferentes partes del mundo.
