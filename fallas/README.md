# Arquitectura de Sistemas: TICS317

---
¡Bienvenidos al repositorio de Arquitectura!. Acá haremos algunos ejercicios complementarios a las clases para profundizar los aprendizajes




# ¿Que necesitamos?
| **Categoría**                  | **Biblioteca**                                                                                          | **Descripción**                                                        |
|-------------------------------|----------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------|
| **1. Manejo de archivos**     | [![json](https://img.shields.io/badge/json-estándar-yellow)](https://docs.python.org/3/library/json.html) | Lectura y escritura de archivos `.json` para almacenar las tareas.     |
| **2. Sistema de archivos**    | [![os](https://img.shields.io/badge/os-estándar-yellow)](https://docs.python.org/3/library/os.html)       | Interacción con el sistema de archivos (opcional, si lo usaste).       |
| **3. Tipado estático**        | [![typing](https://img.shields.io/badge/typing-estándar-yellow)](https://docs.python.org/3/library/typing.html) | Anotaciones de tipo para mayor claridad y validación estática.         |



### El proyecto se desarrolla en:

* Enviroment de Python [![versions](https://img.shields.io/badge/python-3.13-white)](https://www.python.org/downloads/)

* Entorno de Desarrollo Integrado (IDE) [![versions](https://img.shields.io/badge/PyCharm-2024.3.4-white)](https://www.jetbrains.com/help/pycharm/installation-guide.html)

---

# Sistema de Detección de Fallas

## Descripción
Sistema que detecta y monitorea errores HTTP (400, 404, 500) en una aplicación Flask con balanceador de carga.

## Estructura

Cliente → Balanceador (8080) → Servidores Flask (5001, 5002) → Sistema de Logging


## Paso a Paso

### 1. Configurar Sistema de Logging
En `app.py` agregamos:


### 2. Detectar Errores en Endpoints
- **Error 400**: JSON vacío o malformado
- **Error 404**: Recurso no encontrado
- **Error 500**: Errores internos del servidor

### 3. API de Estadísticas
```python
@app.route('/errors/stats')
def error_stats_view():
    return jsonify({
        'total_errors': sum(error_stats.values()),
        'error_types': dict(error_stats),
        'recent_errors': error_log[-10:]
    })
```

## Uso
### Iniciar Sistema

# Terminal 1: Servidor Flask 1
python app.py 5001

# Terminal 2: Servidor Flask 2  
python app.py 5002

# Terminal 3: Balanceador
python load_balancer.py

# Terminal 4: Ejecutar pruebas
python test_errors.py

### Resultado Esperado

Total errores: 3
Tipos de errores: {'400_BAD_REQUEST': 1, '404_NOT_FOUND': 1, '500_INTERNAL_ERROR': 1}

## Endpoints
- `/errors/stats` - Estadísticas de errores
- `/status` - Estado del balanceador
- `/health` - Health check

## Tipos de Errores Detectados

| Código | Tipo | Ejemplo |
| --- | --- | --- |
| 400 | BAD_REQUEST | JSON vacío |
| 404 | NOT_FOUND | Tarea inexistente |
| 500 | INTERNAL_ERROR | División por cero |

## **Propósito de la Detección**

| Error | Cliente | Servidor | Acción |
| --- | --- | --- | --- |
| **400** | ❌ Problema del cliente | ✅ Sistema OK | Validar entrada |
| **404** | ❌ Recurso no existe | ✅ Sistema OK | Verificar endpoint |
| **500** | ✅ Cliente OK | ❌ Problema del servidor | Revisar código |
**Beneficios:**
-  **Monitoreo**: Identificar patrones de errores
-  **Debugging**: Localizar problemas rápidamente
-  **Métricas**: Medir calidad del sistema
-  **Alertas**: Notificar cuando algo falla

El sistema detecta estos errores automáticamente para mantener la **observabilidad** y **confiabilidad** de la aplicación.