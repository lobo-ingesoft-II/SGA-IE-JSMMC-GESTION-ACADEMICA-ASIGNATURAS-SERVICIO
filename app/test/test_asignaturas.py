from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_asignatura():
    response = client.post("/asignaturas/", json={"nombre": "Matemáticas"})
    assert response.status_code == 200
    assert response.json()["nombre"] == "Matemáticas"

def test_get_asignatura():
    response = client.get("/asignaturas/1")
    assert response.status_code == 200
    assert "nombre" in response.json()

def test_list_asignaturas():
    response = client.get("/asignaturas/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
