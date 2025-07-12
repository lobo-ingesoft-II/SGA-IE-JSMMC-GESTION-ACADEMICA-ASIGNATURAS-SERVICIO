from fastapi import FastAPI
from app.routers import asignacion_asignaturas, asignaturas
from fastapi.middleware.cors import CORSMiddleware
from app.db import init_db, test_connection

app = FastAPI(title="Asignaturas API")

@app.on_event("startup")
def startup_event():
    init_db()
    test_connection()

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todas las orígenes
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos HTTP
    allow_headers=["*"],  # Permitir todos los encabezados
)

# Registrar rutas
app.include_router(asignacion_asignaturas.router, prefix="/asignacion_asignaturas", tags=["Asignacion Asignaturas"])
app.include_router(asignaturas.router, prefix="/asignaturas", tags=["Asignaturas"])