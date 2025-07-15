import pytest
# Limpiar la tabla antes de cada test
@pytest.fixture(autouse=True)
def limpiar_tablas():
    db = TestingSessionLocal()
    db.execute("DELETE FROM asignaturas")
    db.commit()
    db.close()
from app.models.asignaturas import Asignatura

import os
import pytest
from unittest.mock import patch, Mock
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db import Base
from app.routers.asignacion_asignaturas import get_db
from fastapi.testclient import TestClient

# Configuración de base de datos temporal SQLite para pruebas
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_temp_asignacion_asignaturas.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

@patch("requests.get")
def test_create_asignacion_asignatura_success(mock_get):
    # Mockear respuestas de servicios externos
    mock_response = Mock()
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    # Crear asignatura de prueba en la base temporal
    db = TestingSessionLocal()
    asignatura = Asignatura()
    asignatura.id_asignatura = 1
    asignatura.nombre = "Matemáticas"
    db.add(asignatura)
    db.commit()
    db.close()

    response = client.post("/asignacion_asignaturas/", json={
        "id_curso": 1,
        "id_asignatura": 1,
        "id_profesor": 1
    })
    assert response.status_code == 200
    assert response.json()["id_curso"] == 1

@patch("requests.get")
def test_create_asignacion_asignatura_error(mock_get):
    # Mockear respuestas de servicios externos
    mock_response = Mock()
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    # Crear asignatura de prueba en la base temporal
    db = TestingSessionLocal()
    asignatura = Asignatura()
    asignatura.id_asignatura = 1
    asignatura.nombre = "Matemáticas"
    db.add(asignatura)
    db.commit()
    db.close()

    response = client.post("/asignacion_asignaturas/", json={
        "id_curso": 1,
        "id_asignatura": 11,
        "id_profesor": 1
    })
    assert response.status_code == 404

def test_get_asignacion_asignatura():
    # Crear asignatura y asignación de prueba en la base temporal
    db = TestingSessionLocal()
    asignatura = Asignatura()
    asignatura.id_asignatura = 2
    asignatura.nombre = "Matemáticas"
    db.add(asignatura)
    db.commit()
    db.close()

    # Crear la asignación usando el endpoint (mock externo)
    with patch("requests.get") as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        client.post("/asignacion_asignaturas/", json={
            "id_curso": 1,
            "id_asignatura": 2,
            "id_profesor": 1
        })

    response = client.get("/asignacion_asignaturas/1")
    assert response.status_code == 200
    assert "id_curso" in response.json()

def test_get_asignacion_error():
    response = client.get("/asignacion_asignaturas/22")
    assert response.status_code == 404

def test_list_asignacion_asignaturas():
    # Crear asignatura y asignación de prueba en la base temporal
    db = TestingSessionLocal()
    asignatura = Asignatura()
    asignatura.id_asignatura = 1
    asignatura.nombre = "Matemáticas"
    db.add(asignatura)
    db.commit()
    db.close()

    # Crear la asignación usando el endpoint (mock externo)
    with patch("requests.get") as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        client.post("/asignacion_asignaturas/", json={
            "id_curso": 1,
            "id_asignatura": 2,
            "id_profesor": 1
        })

    response = client.get("/asignacion_asignaturas/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# Limpiar la base de datos temporal después de las pruebas
def teardown_module(module):
    try:
        os.remove("./test_temp_asignacion_asignaturas.db")
    except FileNotFoundError:
        pass