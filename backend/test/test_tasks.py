import pytest
from fastapi.testclient import TestClient
from bson import ObjectId


def test_create_task(client: TestClient):
    response = client.post(
        "/tasks",
        json={"title": "Learn automated testing"},
    )

    assert response.status_code == 201

    body = response.json()

    assert isinstance(body["id"], str)
    assert body["title"] == "Learn automated testing"
    assert body["completed"] is False


def test_list_tasks(client: TestClient):
    client.post("/tasks", json={"title": "Learn FastAPI"})
    client.post("/tasks", json={"title": "Learn Docker"})

    response = client.get("/tasks")

    assert response.status_code == 200

    body = response.json()

    assert len(body) == 2
    assert isinstance(body[0]["id"], str)
    assert body[0]["title"] == "Learn FastAPI"
    assert body[0]["completed"] is False

    assert isinstance(body[1]["id"], str)
    assert body[1]["title"] == "Learn Docker"
    assert body[1]["completed"] is False


def test_get_task_by_id(client: TestClient):
    created_task = client.post(
        "/tasks",
        json={"title": "Learn path parameters"},
    ).json()

    created_task_id = created_task["id"]
    response = client.get(f"/tasks/{created_task_id}")

    assert response.status_code == 200
    assert response.json() == created_task


def test_get_missing_task_returns_404(client: TestClient):
    response = client.get("/tasks/abc123")

    assert response.status_code == 404


def test_complete_task(client: TestClient):
    created_task = client.post(
        "/tasks",
        json={"title": "Finish Day 5"},
    ).json()

    response = client.patch(
        f"/tasks/{created_task['id']}/complete",
    )

    assert response.status_code == 200

    body = response.json()

    assert isinstance(body["id"], str)
    assert body["title"] == "Finish Day 5"
    assert body["completed"] is True


def test_complete_missing_task_returns_404(client: TestClient):
    response = client.patch("/tasks/999/complete")

    assert response.status_code == 404


def test_delete_task(client: TestClient):
    created_task = client.post(
        "/tasks",
        json={"title": "Delete this task"},
    ).json()

    delete_response = client.delete(
        f"/tasks/{created_task['id']}",
    )

    assert delete_response.status_code == 204

    get_response = client.get(
        f"/tasks/{created_task['id']}",
    )

    assert get_response.status_code == 404


def test_delete_missing_task_returns_404(client: TestClient):
    response = client.delete("/tasks/999")

    assert response.status_code == 404


@pytest.mark.parametrize(
    "bad_title",
    [
        "",
        "   ",
    ],
)
def test_create_task_rejects_blank_title(
    client: TestClient,
    bad_title: str,
):
    response = client.post(
        "/tasks",
        json={"title": bad_title},
    )

    assert response.status_code == 422