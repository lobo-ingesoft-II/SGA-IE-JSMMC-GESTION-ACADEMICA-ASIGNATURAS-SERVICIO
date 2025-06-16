from pydantic import BaseModel
from typing import List

class AsignacionAsignaturaBase(BaseModel):
    id_curso: int
    id_asignatura: int
    id_profesor: int

class AsignacionAsignaturaCreate(AsignacionAsignaturaBase):
    pass

class AsignacionAsignaturaResponse(AsignacionAsignaturaBase):
    id_asignacion: int
    estudiantes: List[int] = None

    class Config:
        orm_mode = True