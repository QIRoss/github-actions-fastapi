import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "GitHub Actions modified this 2!"}

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    assert "version" in response.json()

def test_read_items():
    response = client.get("/items")
    assert response.status_code == 200
    assert len(response.json()) == 2

def test_read_item():
    response = client.get("/items/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["name"] == "Item 1"

def test_read_item_not_found():
    response = client.get("/items/999")
    assert response.status_code == 404

def test_create_item():
    new_item = {
        "id": 3,
        "name": "Item 3",
        "description": "Novo item criado",
        "price": 29.99
    }
    response = client.post("/items", json=new_item)
    assert response.status_code == 200
    assert response.json()["name"] == "Item 3"

def test_create_duplicate_item():
    duplicate_item = {
        "id": 1,
        "name": "Item Duplicado",
        "price": 39.99
    }
    response = client.post("/items", json=duplicate_item)
    assert response.status_code == 400