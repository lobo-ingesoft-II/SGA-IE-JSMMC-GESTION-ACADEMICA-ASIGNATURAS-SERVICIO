# schemas/asignaturas.py
from pydantic import BaseModel

# Clase base común
class AsignaturaBase(BaseModel):
    nombre: str

# Esquema para crear asignaturas (lo que espera el POST)
class AsignaturaCreate(AsignaturaBase):
    pass

# Esquema de respuesta (lo que devuelve el servidor)
class AsignaturaResponse(AsignaturaBase):
    id_asignatura: int

    class Config:
        orm_mode = True

