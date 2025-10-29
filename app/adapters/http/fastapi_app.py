from __future__ import annotations

from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List

from app.domain.task import Task, TaskStatus
from app.application.services.task_service import TaskService
from app.adapters.persistence.memory_task_repository import InMemoryTaskRepository

app = FastAPI(title="Tasks API", version="1.0.0")

_repo_singleton = InMemoryTaskRepository()
_service_singleton = TaskService(_repo_singleton)


def get_task_service() -> TaskService:
    return _service_singleton


class TaskIn(BaseModel):
    title: str = Field(..., min_length=1)
    status: TaskStatus = TaskStatus.pending

    @field_validator("title")
    @classmethod
    def title_non_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("title must be non-empty")
        return v.strip()


class TaskOut(BaseModel):
    id: str
    title: str
    status: TaskStatus

    @classmethod
    def from_domain(cls, task: Task) -> "TaskOut":
        return cls(id=task.id, title=task.title, status=task.status)


class TaskPatch(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1)
    status: Optional[TaskStatus] = None

    @field_validator("title")
    @classmethod
    def title_non_blank_when_present(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        if not v.strip():
            raise ValueError("title must be non-empty when provided")
        return v.strip()


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/tasks", response_model=List[TaskOut])
def list_tasks(svc: TaskService = Depends(get_task_service)):
    tasks = svc.list_tasks()
    return [TaskOut.from_domain(t) for t in tasks]


@app.post("/tasks", status_code=status.HTTP_201_CREATED, response_model=TaskOut)
def create_task(payload: TaskIn, svc: TaskService = Depends(get_task_service)):
    task = svc.create_task(title=payload.title, status=payload.status)
    return TaskOut.from_domain(task)


@app.get("/tasks/{task_id}", response_model=TaskOut)
def get_task(task_id: str, svc: TaskService = Depends(get_task_service)):
    task = svc.get_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskOut.from_domain(task)


@app.put("/tasks/{task_id}", response_model=TaskOut)
def update_task(task_id: str, payload: TaskIn, svc: TaskService = Depends(get_task_service)):
    updated = svc.update_task(task_id, title=payload.title, status=payload.status)
    if updated is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskOut.from_domain(updated)


@app.patch("/tasks/{task_id}", response_model=TaskOut)
def patch_task(task_id: str, payload: TaskPatch, svc: TaskService = Depends(get_task_service)):
    updated = svc.update_task(task_id, title=payload.title, status=payload.status)
    if updated is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskOut.from_domain(updated)


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: str, svc: TaskService = Depends(get_task_service)):
    ok = svc.delete_task(task_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"deleted": True}
