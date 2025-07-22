from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import requests

from app.services.asignacion_asignaturas import get_asignaciones_por_profesor
from app.schemas.asignacion_asignaturas import AsignacionAsignaturaCreate, AsignacionAsignaturaResponse
from app.services.asignacion_asignaturas import create_asignacion_asignatura, get_asignacion_asignatura, list_asignaciones_asignaturas
from app.services.asignacion_asignaturas import get_nombre_asignatura_por_profesor_y_curso, get_nombres_asignaturas_por_profesor_y_curso
from app.schemas.asignacion_asignaturas import AsignaturaNombreResponse
from app.services.asignacion_asignaturas import get_nombres_asignaturas_por_profesor
from app.services.asignaturas import get_asignatura
from app.db import SessionLocal

# Librerias para Observabilidad
from prometheus_client import Counter, Histogram



router = APIRouter()

# 🔧 URLs de las APIs externas
API_CURSOS_URL = "http://sga-cursos-service:8004/cursos"
API_PROFESORES_URL = "http://sga-autenticacion-service:8009/profesor"

# Metricas 
REQUEST_COUNT_ASIGNACION_ASIGNATURAS = Counter(
    "http_requests_total_asignacion_asignaturas", 
    "TOTAL PETICIONES HTTP router-asignaturas",
    ["method", "endpoint"]
)

REQUEST_LATENCY_ASIGNACION_ASIGNATURAS = Histogram(
    "http_request_duration_seconds_asignacion_asignaturas", 
    "DURACION DE LAS PETICIONES router-asignaturas",
    ["method", "endpoint"],
    buckets=[0.1, 0.3, 1.0, 2.5, 5.0, 10.0]  
)

# 3. Errores por endpoint
ERROR_COUNT_ASIGNACION_ASIGNATURAS = Counter(
    "http_request_errors_total_asignacion_asignaturas",
    "TOTAL ERRORES HTTP (status >= 400)",
    ["endpoint", "method", "status_code"]
)

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

@router.get("/por_profesor/{id_profesor}", response_model=list[AsignacionAsignaturaResponse])
def get_by_profesor(id_profesor: int, db: Session = Depends(get_db)):
    asignaciones = get_asignaciones_por_profesor(db, id_profesor)
    if not asignaciones:
        raise HTTPException(status_code=404, detail="No se encontraron asignaciones para este profesor")
    return asignaciones

@router.get("/nombres_asignaturas/por_profesor/{id_profesor}", response_model=list[AsignaturaNombreResponse])
def get_nombres_asignaturas(id_profesor: int, db: Session = Depends(get_db)):
    asignaturas = get_nombres_asignaturas_por_profesor(db, id_profesor)
    if not asignaturas:
        raise HTTPException(status_code=404, detail="No se encontraron asignaturas para este profesor")
    return asignaturas

@router.get("/asignatura/por_profesor_y_curso", response_model=list[AsignaturaNombreResponse])
def get_asignatura_by_profesor_and_curso(id_profesor: int, id_curso: int, db: Session = Depends(get_db)):
    asignaturas = get_nombres_asignaturas_por_profesor_y_curso(db, id_profesor, id_curso)
    if not asignaturas:
        raise HTTPException(status_code=404, detail="No se encontraron asignaturas para este profesor y curso")
    return asignaturas