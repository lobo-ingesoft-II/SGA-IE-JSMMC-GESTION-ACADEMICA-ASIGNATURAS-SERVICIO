from sqlalchemy import Column, Integer, ForeignKey
from app.db import Base

class AsignacionAsignatura(Base):
    __tablename__ = "asignacion_asignaturas"

    id_asignacion = Column(Integer, primary_key=True, index=True)
    id_curso = Column(Integer, nullable=False)
    id_asignatura = Column(Integer, nullable=False)
    id_profesor = Column(Integer, nullable=False)