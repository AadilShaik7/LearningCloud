from fastapi import APIRouter, status, HTTPException
from app.schemas.task import TaskCreate, TaskResponse  
from app.services import task_service
router = APIRouter()

@router.get("/health",status_code=status.HTTP_200_OK)
def health_check() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "learningcloud-api",
    }


@router.post(
    "/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_task(task_create: TaskCreate) -> TaskResponse:
    return task_service.create_task(task_create)


@router.get("/tasks", response_model=list[TaskResponse])
def get_all_tasks() -> list[TaskResponse]:
    return task_service.list_tasks()


@router.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task_by_id(task_id: int) -> TaskResponse:
    task = task_service.get_task(task_id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return task


@router.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_task(task_id: int) -> None:
    if not task_service.delete_task(task_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return None


@router.patch(
    "/tasks/{task_id}/complete",
    response_model=TaskResponse,
)
def complete_task(task_id: int) -> TaskResponse:
    task = task_service.get_task(task_id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    task.completed = True
    return task