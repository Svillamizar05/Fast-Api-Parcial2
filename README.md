# Tasks API (FastAPI + Docker)
## Endpoints
- `GET /health`
- `GET /tasks`
- `POST /tasks` (JSON: `{ "title": "texto", "status": "pending|done" }`)
- Extras: `GET /tasks/{id}`, `PUT /tasks/{id}`, `PATCH /tasks/{id}`, `DELETE /tasks/{id}`

## Ejecución con Docker
```bash
docker build -t api-tareas .
docker run --rm -p 8000:8000 api-tareas

Docs: http://localhost:8000/docs