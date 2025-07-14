from fastapi import FastAPI, Request
from app.routers import asignacion_asignaturas, asignaturas
from fastapi.middleware.cors import CORSMiddleware
from app.db import init_db, test_connection

# Librerias para Observabilidad
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time
from starlette.responses import Response
from app.routers.asignaturas import REQUEST_COUNT_ASIGNATURAS_ROUTERS, REQUEST_LATENCY_ASIGNATURAS_ROUTERS, ERROR_COUNT_ASIGNATURAS_ROUTERS

app = FastAPI(title="ASIGNATURAS API")

# Habilitar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Reemplaza con ["http://localhost:3000"] si deseas restringir
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Middleware para observabilidad
@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start_time = time.time()
    try:
        response = await call_next(request)
        status = response.status_code
    except Exception as e:
        status = 500
        raise e
    finally:
        latency = time.time() - start_time
        endpoint = request.url.path
        method = request.method

        REQUEST_COUNT_ASIGNATURAS_ROUTERS.labels(endpoint=endpoint, method=method).inc()
        REQUEST_LATENCY_ASIGNATURAS_ROUTERS.labels(endpoint=endpoint, method=method).observe(latency)


        
        if status >= 400: # type: ignore
            ERROR_COUNT_ASIGNATURAS_ROUTERS.labels(endpoint=endpoint, method=method, status_code=str(status)).inc() # type: ignore

    return response

# Registrar rutas
app.include_router(asignacion_asignaturas.router, prefix="/asignacion_asignaturas", tags=["Asignacion Asignaturas"])
app.include_router(asignaturas.router, prefix="/asignaturas", tags=["Asignaturas"])