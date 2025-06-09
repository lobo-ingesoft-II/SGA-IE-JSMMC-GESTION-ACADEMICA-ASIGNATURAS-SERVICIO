from pydantic import BaseModel

class AsignacionAsignaturaBase(BaseModel):
    id_curso: int
    id_asignatura: int
    id_profesor: int

class AsignacionAsignaturaCreate(AsignacionAsignaturaBase):
    pass

class AsignacionAsignaturaResponse(AsignacionAsignaturaBase):
    id_asignacion: int

    class Config:
        orm_mode = True