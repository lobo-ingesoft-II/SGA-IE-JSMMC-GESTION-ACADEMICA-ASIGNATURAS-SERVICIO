from sqlalchemy import Column, Integer, ForeignKey,UniqueConstraint
from app.db import Base

class AsignacionAsignatura(Base):
    __tablename__ = "asignacion_asignaturas"

    id_asignacion = Column(Integer, primary_key=True, index=True)
    id_curso = Column(Integer, nullable=False)       # Ya no usa ForeignKey
    id_asignatura = Column(Integer, nullable=False)  # Ya no usa ForeignKey
    id_profesor = Column(Integer, nullable=False)    # Ya no usa ForeignKey

    __table_args__ = (
    UniqueConstraint("id_curso", "id_asignatura", "id_profesor", name="uq_asignacion"),
)
