# Servicio de Asignaturas

## Descripción

Este servicio permite gestionar las asignaturas dentro del sistema académico, tal como su asignación a cursos y profesores. Proporciona funcionalidades para crear, obtener y listar asignaturas y asignación de asignaturas, facilitando su integración con otros módulos del sistema.

## Endpoints

### Crear una asignatura

**POST** `/asignaturas/`

#### Request Body

```json
{
    "nombre": "Matemáticas",
    "estudiantes": [1, 2, 3]
}
```

#### Response

**Status:** 200 OK

```json
{
    "id_asignatura": 1,
    "nombre": "Matemáticas",
    "estudiantes": [1, 2, 3]
}
```

### Obtener una asignatura por ID

**GET** `/asignaturas/{id_asignatura}`

#### Response

**Status:** 200 OK

```json
{
    "id_asignatura": 1,
    "nombre": "Matemáticas",
    "estudiantes": [1, 2, 3]
}
```

**Status:** 404 Not Found

```json
{
    "detail": "Asignatura not found"
}
```

### Listar todas las asignaturas

**GET** `/asignaturas/`

#### Response

**Status:** 200 OK

```json
[
    {
        "id_asignatura": 1,
        "nombre": "Matemáticas",
        "estudiantes": [1, 2, 3]
    },
    {
        "id_asignatura": 2,
        "nombre": "Historia",
        "estudiantes": [1, 2, 3]
    }
]
```

### Asignar una asignatura a un usuario

**POST** `/asignacion_asignaturas/`

#### Request Body

```json
{
  "id_curso": 1,
  "id_asignatura": 1,
  "id_profesor": 1
}
```

#### Response

**Status:** 200 OK

```json
{
  "id_asignacion": 1,
  "id_curso": 1,
  "id_asignatura": 1,
  "id_profesor": 1
}
```

### Obtener asignaciones de un usuario

**GET** `/asignacion_asignaturas/{id_asignacion}`

#### Response

**Status:** 200 OK

```json
{
  "id_asignacion": 1,
  "id_curso": 1,
  "id_asignatura": 1,
  "id_profesor": 1
}
```

**Status:** 404 Not found

```json
{
  "detail": "Asignacion not found"
}
```

### Listar todas las asignaciones

**GET** `/asignacion_asignaturas/`

#### Response

**Status:** 200 OK

```json
[
  {
    "id_asignacion": 1,
    "id_curso": 1,
    "id_asignatura": 1,
    "id_profesor": 1
  },
  {
    "id_asignacion": 2,
    "id_curso": 2,
    "id_asignatura": 2,
    "id_profesor": 2
  }
]
```

## Instalación

1. Asegúrate de tener el entorno configurado:

     ```bash
     pip install -r requirements.txt
     ```
2. Configura la base de datos en el archivo `.env`:

     ```env
     DATABASE_URL="mysql+pymysql://user:password@host:port/database"
     ```
3. Ejecuta el servidor:

     ```bash
     uvicorn app.main:app --reload --port 8001
     ```

## Pruebas

Para ejecutar las pruebas unitarias:

```bash
pytest app/tests/test_asignaturas.py
```

## Dependencias

* **FastAPI**: Framework principal.
* **SQLAlchemy**: ORM para manejar la base de datos.
* **Pytest**: Framework para pruebas unitarias.

## Documentación interactiva

Accede a la documentación Swagger en [http://localhost:8001/docs](http://localhost:8001/docs) o ReDoc en [http://localhost:8001/redoc](http://localhost:8001/redoc).

## Contacto

Para más información, contactar con el equipo de desarrollo.
