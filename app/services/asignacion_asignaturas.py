from sqlalchemy.orm import Session
from app.models.asignacion_asignaturas import AsignacionAsignatura
from app.schemas.asignacion_asignaturas import AsignacionAsignaturaCreate

def create_asignacion_asignatura(db: Session, asignacion: AsignacionAsignaturaCreate):
    db_asignacion = AsignacionAsignatura(**asignacion.dict())
    db.add(db_asignacion)
    db.commit()
    db.refresh(db_asignacion)
    return db_asignacion

def get_asignacion_asignatura(db: Session, id_asignacion: int):
    return db.query(AsignacionAsignatura).filter(AsignacionAsignatura.id_asignacion == id_asignacion).first()

def list_asignaciones_asignaturas(db: Session):
    return db.query(AsignacionAsignatura).all()