import pytest
from fastapi.testclient import TestClient

from app.services import task_service
from app.main import app

@pytest.fixture(autouse=True)
def reset_data():
    task_service.temp_db.clear()
    task_service.next_task_id = 1

@pytest.fixture()
def client():
    with TestClient(app) as test_client:
        yield test_client