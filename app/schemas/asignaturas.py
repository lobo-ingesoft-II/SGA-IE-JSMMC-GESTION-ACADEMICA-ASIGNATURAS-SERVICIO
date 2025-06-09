from pydantic import BaseModel

class AsignaturaBase(BaseModel):
    nombre: str | None

class AsignaturaCreate(AsignaturaBase):
    pass

class AsignaturaResponse(AsignaturaBase):
    id_asignatura: int

    class Config:
        orm_mode = True