import pytest
from app import app

@pytest.fixture
def client():
    return app.test_client()

def test_home(client):
    """Check if the home page loads"""
    response = client.get('/')
    assert response.status_code == 200
    assert b"ACEest Fitness" in response.data