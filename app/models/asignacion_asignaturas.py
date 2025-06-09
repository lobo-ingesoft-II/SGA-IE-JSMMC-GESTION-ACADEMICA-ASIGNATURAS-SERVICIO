from sqlalchemy import Column, Integer, ForeignKey
from app.db import Base

class AsignacionAsignatura(Base):
    __tablename__ = "asignacion_asignaturas"

    id_asignacion = Column(Integer, primary_key=True, index=True)
    id_curso = Column(Integer, ForeignKey("cursos.id_curso"), nullable=False)
    id_asignatura = Column(Integer, ForeignKey("asignaturas.id_asignatura"), nullable=False)
    id_profesor = Column(Integer, ForeignKey("profesores.id_profesor"), nullable=False)