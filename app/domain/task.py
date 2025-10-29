from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
import uuid


class TaskStatus(str, Enum):
    pending = "pending"
    done = "done"


@dataclass(frozen=True, slots=True)
class Task:
    id: str
    title: str
    status: TaskStatus = field(default=TaskStatus.pending)

    def with_updates(self, *, title: Optional[str] = None, status: Optional[TaskStatus] = None) -> "Task":
        return Task(
            id=self.id,
            title=title if title is not None else self.title,
            status=status if status is not None else self.status,
        )


class TaskFactory:
    @staticmethod
    def create(title: str, status: TaskStatus = TaskStatus.pending) -> Task:
        title_clean = (title or "").strip()
        if not title_clean:
            raise ValueError("title must be a non-empty string")
        if status not in (TaskStatus.pending, TaskStatus.done):
            raise ValueError("status must be 'pending' or 'done'")
        return Task(id=str(uuid.uuid4()), title=title_clean, status=status)
