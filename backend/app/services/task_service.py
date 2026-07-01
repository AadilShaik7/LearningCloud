from app.schemas.task import TaskCreate, TaskResponse

temp_db: dict[int, TaskResponse] = {}
next_task_id = 1


def create_task(task_create: TaskCreate) -> TaskResponse:
    global next_task_id

    task_response = TaskResponse(
        id=next_task_id,
        title=task_create.title,
        completed=False,
    )

    temp_db[task_response.id] = task_response
    next_task_id += 1

    return task_response


def list_tasks() -> list[TaskResponse]:
    return list(temp_db.values())


def get_task(task_id: int) -> TaskResponse | None:
    return temp_db.get(task_id)


def complete_task(task_id: int) -> TaskResponse | None:
    task = temp_db.get(task_id)

    if task is None:
        return None

    completed_task = task.model_copy(
        update={"completed": True},
    )

    temp_db[task_id] = completed_task

    return completed_task


def delete_task(task_id: int) -> bool:
    if task_id not in temp_db:
        return False

    del temp_db[task_id]

    return True