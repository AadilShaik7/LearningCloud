import pytest
from fastapi.testclient import TestClient
from app.database import tasks_collection
from app.services import task_service
from app.main import app

@pytest.fixture(autouse=True)
def reset_data():
    tasks_collection.delete_many({})

@pytest.fixture()
def client():
    with TestClient(app) as test_client:
        yield test_client