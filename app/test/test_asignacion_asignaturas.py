from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_asignacion_asignatura():
    response = client.post("/asignacion_asignaturas/", json={
        "id_curso": 1,
        "id_asignatura": 1,
        "id_profesor": 1
    })
    assert response.status_code == 200
    assert response.json()["id_curso"] == 1

def test_get_asignacion_asignatura():
    response = client.get("/asignacion_asignaturas/1")
    assert response.status_code == 200
    assert "id_curso" in response.json()

def test_list_asignacion_asignaturas():
    response = client.get("/asignacion_asignaturas/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)