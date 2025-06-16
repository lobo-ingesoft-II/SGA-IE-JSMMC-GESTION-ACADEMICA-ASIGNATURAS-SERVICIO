from sqlalchemy.orm import Session
from app.models.asignaturas import Asignatura
from app.schemas.asignaturas import AsignaturaCreate

def create_asignatura(db, asignatura: AsignaturaCreate):
    db_asignatura = Asignatura(
        nombre=asignatura.nombre,
        estudiantes=asignatura.estudiantes
    )
    db.add(db_asignatura)
    db.commit()
    db.refresh(db_asignatura)
    return db_asignatura

def get_asignatura(db: Session, id_asignatura: int):
    return db.query(Asignatura).filter(Asignatura.id_asignatura == id_asignatura).first()

def list_asignaturas(db: Session):
    return db.query(Asignatura).all()