from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.asignaturas import AsignaturaCreate, AsignaturaResponse
from app.services.asignaturas import create_asignatura, get_asignatura, list_asignaturas
from app.db import SessionLocal

router = APIRouter()

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