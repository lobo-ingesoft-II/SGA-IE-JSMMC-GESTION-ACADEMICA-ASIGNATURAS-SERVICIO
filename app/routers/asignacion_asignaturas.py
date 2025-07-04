from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import requests

from app.schemas.asignacion_asignaturas import AsignacionAsignaturaCreate, AsignacionAsignaturaResponse
from app.services.asignacion_asignaturas import create_asignacion_asignatura, get_asignacion_asignatura, list_asignaciones_asignaturas
from app.services.asignaturas import get_asignatura
from app.db import SessionLocal

router = APIRouter()

# 🔧 URLs de las APIs externas
API_CURSOS_URL = "http://127.0.0.1:8002/cursos"
API_PROFESORES_URL = "http://127.0.0.1:8009/profesores"

# 🔁 Generador de conexión a base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ CREAR una asignación
@router.post("/", response_model=AsignacionAsignaturaResponse)
def create(asignacion: AsignacionAsignaturaCreate, db: Session = Depends(get_db)):

    # 1. Verificar existencia de la asignatura
    db_asignatura = get_asignatura(db, asignacion.id_asignatura)
    if not db_asignatura:
        raise HTTPException(status_code=404, detail="Asignatura no encontrada")

    # 2. Verificar existencia del curso
    curso_response = requests.get(f"{API_CURSOS_URL}/{asignacion.id_curso}")
    if curso_response.status_code != 200:
        raise HTTPException(status_code=404, detail="Curso no encontrado")

    # 3. Verificar existencia del profesor
    profesor_response = requests.get(f"{API_PROFESORES_URL}/{asignacion.id_profesor}")
    if profesor_response.status_code != 200:
        raise HTTPException(status_code=404, detail="Profesor no encontrado")

    # 4. Crear la asignación si todo está bien
    return create_asignacion_asignatura(db, asignacion)

# ✅ OBTENER una asignación por ID
@router.get("/{id_asignacion}", response_model=AsignacionAsignaturaResponse)
def get(id_asignacion: int, db: Session = Depends(get_db)):
    db_asignacion = get_asignacion_asignatura(db, id_asignacion)
    if not db_asignacion:
        raise HTTPException(status_code=404, detail="Asignación no encontrada")
    return db_asignacion

# ✅ LISTAR asignaciones
@router.get("/", response_model=list[AsignacionAsignaturaResponse])
def list_all(db: Session = Depends(get_db)):
    return list_asignaciones_asignaturas(db)
