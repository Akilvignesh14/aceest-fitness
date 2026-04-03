import pytest
from app import app
import os
import sqlite3

# Define the test database name
DB_NAME = "test_fitness.db"

@pytest.fixture
def client():
    app.config['TESTING'] = True
    
    # Initialize a clean test DB
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS clients (id INTEGER PRIMARY KEY, name TEXT, program TEXT, membership TEXT)")
    cur.execute("INSERT INTO clients (name, program, membership) VALUES ('Tester', 'Muscle Gain', 'Active')")
    conn.commit()
    conn.close()

    with app.test_client() as client:
        yield client
    
    # Cleanup after test - SRE Practice: Leave the environment clean
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)

def test_home_status(client):
    """Phase 3: Validate logic of the home endpoint"""
    res = client.get('/')
    assert res.status_code == 200
    assert b"ACEest Fitness System Online" in res.data

def test_get_client_data(client):
    """Phase 3: Validate client retrieval logic"""
    res = client.get('/client/Tester')
    assert res.status_code == 200
    data = res.get_json()
    assert data['name'] == 'Tester'
    assert data['program'] == 'Muscle Gain'

def test_client_not_found(client):
    """Phase 3: Validate error handling (Negative Testing)"""
    res = client.get('/client/UnknownUser')
    assert res.status_code == 404