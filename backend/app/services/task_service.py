import os

from dotenv import load_dotenv

from app.schemas.task import TaskCreate, TaskResponse

load_dotenv()

tasks_backend = os.getenv("TASKS_BACKEND", "mongodb").lower()

if tasks_backend == "dynamodb":
    from app.services import dynamodb_task_service as selected_service
else:
    from app.services import mongodb_task_service as selected_service


def create_task(task_create: TaskCreate) -> TaskResponse:
    return selected_service.create_task(task_create)


def list_tasks() -> list[TaskResponse]:
    return selected_service.list_tasks()


def get_task(task_id: str) -> TaskResponse | None:
    return selected_service.get_task(task_id)


def complete_task(task_id: str) -> TaskResponse | None:
    return selected_service.complete_task(task_id)


def delete_task(task_id: str) -> bool:
    return selected_service.delete_task(task_id)