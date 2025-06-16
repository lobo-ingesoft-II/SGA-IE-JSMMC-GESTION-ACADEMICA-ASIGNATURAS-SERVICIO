from pydantic import BaseModel
from typing import List

class AsignaturaBase(BaseModel):
    nombre: str | None

class AsignaturaCreate(AsignaturaBase):
    estudiantes: List[int] = []


class AsignaturaResponse(AsignaturaBase):
    id_asignatura: int
    estudiantes: List[int] = []

    class Config:
        orm_mode = True