import pytest
import os
import sqlite3

# CRITICAL: Set environment variable BEFORE importing the app
os.environ["DB_NAME"] = "test_fitness.db"

from app import app, DB_NAME

@pytest.fixture
def client():
    """Phase 3: Unit Testing & Validation Framework"""
    app.config['TESTING'] = True
    
    # Setup: Initialize a clean, isolated test database
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS clients (id INTEGER PRIMARY KEY, name TEXT, program TEXT, membership TEXT)")
    # Inject 'Tester' so the retrieval test can find it
    cur.execute("INSERT INTO clients (name, program, membership) VALUES ('Tester', 'Muscle Gain', 'Active')")
    conn.commit()
    conn.close()

    with app.test_client() as client:
        yield client
    
    # Teardown: SRE Principle - Clean the environment after tests
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)

def test_home_status(client):
    """Validate the status endpoint logic"""
    res = client.get('/')
    assert res.status_code == 200
    assert b"ACEest Fitness System Online" in res.data

def test_get_client_data(client):
    """Validate client retrieval logic - Success Case"""
    res = client.get('/client/Tester')
    assert res.status_code == 200
    data = res.get_json()
    assert data['name'] == 'Tester'
    assert data['program'] == 'Muscle Gain'

def test_client_not_found(client):
    """Validate error handling logic - Negative Case"""
    res = client.get('/client/UnknownUser')
    assert res.status_code == 404