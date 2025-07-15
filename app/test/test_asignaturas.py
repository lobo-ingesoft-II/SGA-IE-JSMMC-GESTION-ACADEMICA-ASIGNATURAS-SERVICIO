
import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db import Base
from app.routers.asignaturas import get_db
from fastapi.testclient import TestClient

# Configuración de base de datos temporal SQLite para pruebas
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_temp_asignaturas.db"
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

# Limpiar la base de datos temporal después de las pruebas
def teardown_module(module):
    try:
        os.remove("./test_temp_asignaturas.db")
    except FileNotFoundError:
        pass
