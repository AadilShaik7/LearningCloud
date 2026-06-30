from fastapi import FastAPI, HTTPException, status

from app.schemas.task import TaskCreate, TaskResponse

app = FastAPI(
    title="Learning Cloud",
    version="0.1.0",
)

temp_db: dict[int, TaskResponse] = {}
next_id = 0


@app.get("/health")
def health_check() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "learningcloud-api",
    }


@app.post(
    "/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_task(task_create: TaskCreate) -> TaskResponse:
    global next_id

    task_response = TaskResponse(
        id=next_id,
        title=task_create.title,
        completed=False,
    )

    temp_db[task_response.id] = task_response
    next_id += 1

    return task_response


@app.get("/tasks", response_model=list[TaskResponse])
def get_all_tasks() -> list[TaskResponse]:
    return list(temp_db.values())


@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task_by_id(task_id: int) -> TaskResponse:
    task = temp_db.get(task_id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return task


@app.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_task(task_id: int) -> None:
    if task_id not in temp_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    del temp_db[task_id]
    return None


@app.patch(
    "/tasks/{task_id}/complete",
    response_model=TaskResponse,
)
def complete_task(task_id: int) -> TaskResponse:
    task = temp_db.get(task_id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    task.completed = True
    return task