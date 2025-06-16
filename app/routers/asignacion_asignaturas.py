from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.asignacion_asignaturas import AsignacionAsignaturaCreate, AsignacionAsignaturaResponse
from app.services.asignacion_asignaturas import create_asignacion_asignatura, get_asignacion_asignatura, list_asignaciones_asignaturas
from app.services.asignaturas import get_asignatura
from app.db import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=AsignacionAsignaturaResponse)
def create(asignacion: AsignacionAsignaturaCreate, db: Session = Depends(get_db)):
    return create_asignacion_asignatura(db, asignacion)

@router.get("/{id_asignacion}", response_model=AsignacionAsignaturaResponse)
def get(id_asignacion: int, db: Session = Depends(get_db)):
    db_asignacion = get_asignacion_asignatura(db, id_asignacion)
    if not db_asignacion:
        raise HTTPException(status_code=404, detail="Asignacion not found")
    # Buscar la asignatura asociada y obtener estudiantes
    db_asignatura = get_asignatura(db, db_asignacion.id_asignatura)
    estudiantes = db_asignatura.estudiantes if db_asignatura else []
    # Convertir a dict y agregar estudiantes
    response = AsignacionAsignaturaResponse.from_orm(db_asignacion)
    response.estudiantes = estudiantes
    return response

@router.get("/", response_model=list[AsignacionAsignaturaResponse])
def list_all(db: Session = Depends(get_db)):
    return list_asignaciones_asignaturas(db)