import os
from uuid import uuid4

import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv

from app.schemas.task import TaskCreate, TaskResponse

load_dotenv()

aws_region = os.getenv("AWS_REGION", "us-east-2")
table_name = os.getenv("DYNAMODB_TABLE_NAME")

if not table_name:
    raise RuntimeError(
        "DYNAMODB_TABLE_NAME is missing. Add it to your environment variables."
    )

dynamodb = boto3.resource("dynamodb", region_name=aws_region)
tasks_table = dynamodb.Table(table_name)


def document_to_response(task_document: dict) -> TaskResponse:
    return TaskResponse(
        id=task_document["task_id"],
        title=task_document["title"],
        completed=task_document["completed"],
    )


def create_task(task_create: TaskCreate) -> TaskResponse:
    task_id = str(uuid4())

    task_document = {
        "task_id": task_id,
        "title": task_create.title,
        "completed": False,
    }

    tasks_table.put_item(Item=task_document)

    return document_to_response(task_document)


def list_tasks() -> list[TaskResponse]:
    response = tasks_table.scan()
    items = response.get("Items", [])

    return [document_to_response(item) for item in items]


def get_task(task_id: str) -> TaskResponse | None:
    response = tasks_table.get_item(
        Key={
            "task_id": task_id,
        }
    )

    task_document = response.get("Item")
    if task_document is None:
        return None

    return document_to_response(task_document)


def complete_task(task_id: str) -> TaskResponse | None:
    try:
        response = tasks_table.update_item(
            Key={
                "task_id": task_id,
            },
            UpdateExpression="SET completed = :completed",
            ExpressionAttributeValues={
                ":completed": True,
            },
            ConditionExpression="attribute_exists(task_id)",
            ReturnValues="ALL_NEW",
        )
    except ClientError as error:
        error_code = error.response["Error"]["Code"]

        if error_code == "ConditionalCheckFailedException":
            return None

        raise

    updated_document = response["Attributes"]
    return document_to_response(updated_document)


def delete_task(task_id: str) -> bool:
    try:
        tasks_table.delete_item(
            Key={
                "task_id": task_id,
            },
            ConditionExpression="attribute_exists(task_id)",
        )
    except ClientError as error:
        error_code = error.response["Error"]["Code"]

        if error_code == "ConditionalCheckFailedException":
            return False

        raise

    return True