from sqlalchemy.orm import Session
from app.models.asignacion_asignaturas import AsignacionAsignatura
from app.schemas.asignacion_asignaturas import AsignacionAsignaturaCreate
from app.models.asignacion_asignaturas import AsignacionAsignatura
from app.models.asignaturas import Asignatura

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

def get_asignaciones_por_profesor(db: Session, id_profesor: int):
    return db.query(AsignacionAsignatura).filter(AsignacionAsignatura.id_profesor == id_profesor).all()

def get_nombres_asignaturas_por_profesor(db: Session, id_profesor: int):
    return (
        db.query(Asignatura.nombre)
        .join(AsignacionAsignatura, Asignatura.id_asignatura == AsignacionAsignatura.id_asignatura)
        .filter(AsignacionAsignatura.id_profesor == id_profesor)
        .all()
    )

def get_nombre_asignatura_por_profesor_y_curso(db: Session, id_profesor: int, id_curso: int):
    resultado = (
        db.query(Asignatura.nombre)
        .join(AsignacionAsignatura, AsignacionAsignatura.id_asignatura == Asignatura.id_asignatura)
        .filter(
            AsignacionAsignatura.id_profesor == id_profesor,
            AsignacionAsignatura.id_curso == id_curso
        )
        .first()
    )
    return resultado

def get_nombres_asignaturas_por_profesor_y_curso(db: Session, id_profesor: int, id_curso: int):
    """Obtiene TODAS las asignaturas asociadas a un profesor y curso específico"""
    resultado = (
        db.query(Asignatura.nombre)
        .join(AsignacionAsignatura, AsignacionAsignatura.id_asignatura == Asignatura.id_asignatura)
        .filter(
            AsignacionAsignatura.id_profesor == id_profesor,
            AsignacionAsignatura.id_curso == id_curso
        )
        .all()
    )
    return resultado