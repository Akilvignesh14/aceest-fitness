import pytest
from app import app

@pytest.fixture
def client():
    return app.test_client()

def test_programs_data(client):
    """Test that our modularized gym data is loading correctly"""
    response = client.get('/programs')
    assert response.status_code == 200
    # Check if 'Fat Loss' exists in the data we sent
    assert b"Fat Loss" in response.data