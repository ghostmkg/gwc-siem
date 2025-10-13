
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app import db
from app.models import Alert
from datetime import datetime

# Use a test-specific database
TEST_DATABASE = "test_alerts.db"
db.DATABASE = TEST_DATABASE

@pytest.fixture(autouse=True)
def setup_and_teardown_database():
    # Setup: create a clean database before each test
    db.init_db()
    yield
    # Teardown: clean up the database after each test
    import os
    os.remove(TEST_DATABASE)

client = TestClient(app)

def test_get_alerts_empty():
    response = client.get("/alerts")
    assert response.status_code == 200
    assert response.json() == []

def test_get_alerts_with_data():
    # Add some dummy data
    alert1 = Alert(timestamp=datetime.now(), rule_name="Test Rule 1", description="Test Desc 1", source_ip="1.1.1.1")
    alert2 = Alert(timestamp=datetime.now(), rule_name="Test Rule 2", description="Test Desc 2", source_ip="2.2.2.2")
    db.add_alert(alert1)
    db.add_alert(alert2)

    response = client.get("/alerts")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["rule_name"] == "Test Rule 2" # Note: alerts are returned in descending order

def test_get_alerts_with_limit():
    # Add some dummy data
    for i in range(5):
        alert = Alert(timestamp=datetime.now(), rule_name=f"Test Rule {i}", description=f"Test Desc {i}", source_ip=f"1.1.1.{i}")
        db.add_alert(alert)

    response = client.get("/alerts?limit=3")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
