from fastapi import FastAPI
from app.routers import asignacion_asignaturas, asignaturas
from app.db import init_db, test_connection

app = FastAPI(title="Asignaturas API")

@app.on_event("startup")
def startup_event():
    init_db()
    test_connection()

# Registrar rutas
app.include_router(asignacion_asignaturas.router, prefix="/asignacion_asignaturas", tags=["Asignacion Asignaturas"])
app.include_router(asignaturas.router, prefix="/asignaturas", tags=["Asignaturas"])