from __future__ import annotations
from typing import Iterable, Optional
from app.domain.task import Task, TaskFactory, TaskStatus
from app.application.ports.task_repository import TaskRepository


class TaskService:
    def __init__(self, repo: TaskRepository):
        self._repo = repo

    def list_tasks(self) -> Iterable[Task]:
        return self._repo.list()

    def create_task(self, *, title: str, status: TaskStatus) -> Task:
        task = TaskFactory.create(title=title, status=status)
        return self._repo.add(task)

    def get_task(self, task_id: str) -> Optional[Task]:
        return self._repo.get(task_id)

    def update_task(self, task_id: str, *, title: Optional[str] = None, status: Optional[TaskStatus] = None) -> Optional[Task]:
        current = self._repo.get(task_id)
        if current is None:
            return None
        updated = current.with_updates(title=title, status=status)
        return self._repo.update(updated)

    def delete_task(self, task_id: str) -> bool:
        existing = self._repo.get(task_id)
        if existing is None:
            return False
        self._repo.delete(task_id)
        return True
