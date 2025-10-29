# Tasks API (FastAPI + Docker)

Examen de Arquitectura de Software — Parte Práctica 70% (29-Oct-2025).  
Proyecto construido con **FastAPI**, principios **SOLID** y patrones simples (**Repository**, **Service/Use Case**). Ejecutable con **Docker** en el puerto **8000**.

---

## ✨ Objetivo
Una API REST de **tareas** con persistencia **en memoria** (intercambiable a futuro), diseño por capas y contenedorización.

---

## ✅ Endpoints implementados
| Método | Ruta                | Descripción                |
|-------:|---------------------|----------------------------|
|  GET   | `/health`           | Estado del servicio        |
|  GET   | `/tasks`            | Listar tareas              |
|  POST  | `/tasks`            | Crear tarea                |
|  GET   | `/tasks/{task_id}`  | Obtener una tarea por ID   |
|  PUT   | `/tasks/{task_id}`  | Actualizar **total**       |
| PATCH  | `/tasks/{task_id}`  | Actualizar **parcial**     |
| DELETE | `/tasks/{task_id}`  | Eliminar tarea             |

---

## Estructura de Carpetas
app/
  domain/
    task.py
  application/
    ports/
      task_repository.py
    services/
      task_service.py
  adapters/
    http/
      fastapi_app.py
    persistence/
      memory_task_repository.py
Dockerfile
requirements.txt
README.md
---
## 🐳 Ejecutar con Docker
### Build
```bash
docker build -t tasks-api:1.0 .
```
### Run (un solo comando)
```bash
docker run --rm -p 8000:8000 tasks-api:1.0
```
### Docs: http://localhost:8000/docs
---
## 🔌 Ejemplos de Uso (curl)
### Salud
curl -s http://localhost:8000/health | jq .

### Listar tareas
```bash
curl -s http://localhost:8000/tasks | jq .
# []
```
### Crear tarea
```bash
curl -s -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Comprar leche","status":"pending"}' | jq .
```
### Obtener por ID
```bash
TASK_ID="pega-el-id-aqui"
curl -s http://localhost:8000/tasks/$TASK_ID | jq .
```

### Actualización TOTAL (PUT)
```bash
curl -s -X PUT http://localhost:8000/tasks/$TASK_ID \
  -H "Content-Type: application/json" \
  -d '{"title":"Comprar leche descremada","status":"done"}' | jq .
```

### Actualización PARCIAL (PATCH)
```bash
curl -s -X PATCH http://localhost:8000/tasks/$TASK_ID \
  -H "Content-Type: application/json" \
  -d '{"status":"done"}' | jq .
```

### Eliminar
```bash
curl -s -X DELETE http://localhost:8000/tasks/$TASK_ID | jq .
# { "deleted": true }
```
---
