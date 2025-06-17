from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.schemas.asignacion_asignaturas import AsignacionAsignaturaCreate, AsignacionAsignaturaResponse
from app.services.asignacion_asignaturas import create_asignacion_asignatura, get_asignacion_asignatura, list_asignaciones_asignaturas
from app.db import SessionLocal
from app.models.asignacion_asignaturas import AsignacionAsignatura

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
    return db_asignacion

@router.get("/", response_model=list[AsignacionAsignaturaResponse])
def list_all(db: Session = Depends(get_db)):
    return list_asignaciones_asignaturas(db)

@router.get("/filtrar/", response_model=list[int])
def filtrar_asignaturas(
    id_curso: int = Query(..., description="ID del curso"),
    id_profesor: int = Query(..., description="ID del profesor"),
    db: Session = Depends(get_db)
):
    asignaciones = db.query(AsignacionAsignatura).filter(
        AsignacionAsignatura.id_curso == id_curso,
        AsignacionAsignatura.id_profesor == id_profesor
    ).all()
    return [a.id_asignatura for a in asignaciones]