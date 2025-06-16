from sqlalchemy import Column, Integer, String, BigInteger
from sqlalchemy.dialects.postgresql import ARRAY
from app.db import Base

class Asignatura(Base):
    __tablename__ = "asignaturas"

    id_asignatura = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=True)
    estudiantes = Column(ARRAY(BigInteger), nullable=True)