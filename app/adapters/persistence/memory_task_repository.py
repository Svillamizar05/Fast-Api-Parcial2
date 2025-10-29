from __future__ import annotations
from typing import Dict, Iterable, Optional
from app.domain.task import Task


class InMemoryTaskRepository:
    def __init__(self):
        self._data: Dict[str, Task] = {}

    def list(self) -> Iterable[Task]:
        return list(self._data.values())

    def get(self, task_id: str) -> Optional[Task]:
        return self._data.get(task_id)

    def add(self, task: Task) -> Task:
        self._data[task.id] = task
        return task

    def update(self, task: Task) -> Task:
        if task.id not in self._data:
            raise KeyError(f"Task {task.id} not found")
        self._data[task.id] = task
        return task

    def delete(self, task_id: str) -> None:
        self._data.pop(task_id, None)
