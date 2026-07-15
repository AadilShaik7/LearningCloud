from pymongo import ReturnDocument

from app.schemas.task import TaskCreate, TaskResponse
from app.database import tasks_collection
from bson import ObjectId


def sanitize_object_id(id: str) -> str | None:
    if not ObjectId.is_valid(id):
        return None
    return ObjectId(id)

def create_task(task_create: TaskCreate) -> TaskResponse:

    task_document = {
    "title": task_create.title,
    "completed": False,
}
    
    insert_result = tasks_collection.insert_one(task_document)

    task_response = TaskResponse(
        id = str(insert_result.inserted_id),
        title = task_document["title"],
        completed = task_document["completed"],
    )

    return task_response


def list_tasks() -> list[TaskResponse]:
    task_documents = tasks_collection.find({})
    return [TaskResponse(id=str(task["_id"]), title=task["title"], completed=task["completed"]) for task in task_documents]


def get_task(task_id: str) -> TaskResponse | None:
    object_id = sanitize_object_id(task_id)
    if object_id is None:
        return None
    task_document = tasks_collection.find_one({"_id": object_id})
    if not task_document:
        return None
    return TaskResponse(id=str(task_document["_id"]), title=task_document["title"], completed=task_document["completed"])


def complete_task(task_id: str) -> TaskResponse | None:
    object_id = sanitize_object_id(task_id)

    if object_id is None:
        return None

    task_document = tasks_collection.find_one_and_update(
        {"_id": object_id},
        {"$set": {"completed": True}},
        return_document=ReturnDocument.AFTER,
    )
    
    if task_document is None:
        return None
    
    return TaskResponse(
        id=str(task_document["_id"]),
        title=task_document["title"],
        completed=task_document["completed"],
    )


def delete_task(task_id: str) -> bool:
    object_id = sanitize_object_id(task_id)
    if object_id is None:
        return False
    task_document = tasks_collection.find_one_and_delete({"_id": object_id})
    return task_document is not None