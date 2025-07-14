from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.asignaturas import AsignaturaCreate, AsignaturaResponse
from app.services.asignaturas import create_asignatura, get_asignatura, list_asignaturas
from app.db import SessionLocal

# Librerias para Observabilidad
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time
from starlette.responses import Response
from prometheus_client import CollectorRegistry, generate_latest


router = APIRouter()

# Metricas 
REQUEST_COUNT_ASIGNATURAS_ROUTERS = Counter(
    "http_requests_total", 
    "TOTAL PETICIONES HTTP router-asignaturas",
    ["method", "endpoint"]
)

REQUEST_LATENCY_ASIGNATURAS_ROUTERS = Histogram(
    "http_request_duration_seconds", 
    "DURACION DE LAS PETICIONES router-asinaturas",
    ["method", "endpoint"],
    buckets=[0.1, 0.3, 1.0, 2.5, 5.0, 10.0]  
)

# 3. Errores por endpoint
ERROR_COUNT_ASIGNATURAS_ROUTERS = Counter(
    "http_request_errors_total",
    "TOTAL ERRORES HTTP (status >= 400)",
    ["endpoint", "method", "status_code"]
)

# Ruta para observabilidad 
@router.get("/custom_metrics")
def custom_metrics():
    registry = CollectorRegistry()
    registry.register(REQUEST_COUNT_ASIGNATURAS_ROUTERS)
    registry.register(REQUEST_LATENCY_ASIGNATURAS_ROUTERS)
    registry.register(ERROR_COUNT_ASIGNATURAS_ROUTERS)
    return Response(generate_latest(registry), media_type=CONTENT_TYPE_LATEST)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=AsignaturaResponse)
def create(asignatura: AsignaturaCreate, db: Session = Depends(get_db)):
    return create_asignatura(db, asignatura)

@router.get("/{id_asignatura}", response_model=AsignaturaResponse)
def get(id_asignatura: int, db: Session = Depends(get_db)):
    db_asignatura = get_asignatura(db, id_asignatura)
    if not db_asignatura:
        raise HTTPException(status_code=404, detail="Asignatura not found")
    return db_asignatura

@router.get("/", response_model=list[AsignaturaResponse])
def list_all(db: Session = Depends(get_db)):
    return list_asignaturas(db)