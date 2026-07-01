import pytest
from fastapi.testclient import TestClient

import app.main as main
from app.main import app

@pytest.fixture(autouse=True)
def reset_data():
    main.temp_db.clear()
    main.next_id = 1

@pytest.fixture()
def client():
    with TestClient(app) as test_client:
        yield test_client