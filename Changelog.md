# Changelog - Servicio de Asignaturas

## \[1.0.0] - 2025-06-09

### Agregado

* Creación del servicio de asignaturas.
* Endpoint **POST** `/asignaturas/` para agregar una nueva asignatura.
* Endpoint **GET** `/asignaturas/{id_asignatura}` para obtener una asignatura por su ID.
* Endpoint **GET** `/asignaturas/` para listar todas las asignaturas.
* Integración de modelos, esquemas y servicios con SQLAlchemy y Pydantic.
* Pruebas unitarias básicas para las operaciones CRUD de asignaturas.

## \[1.0.1] - 2025-06-09

### Corregido

* Mejora en la validación de datos para nombres nulos en las asignaturas.

## \[1.1.0] - 2025-06-10

### Agregado

* Endpoint **POST** `/asignacion_asignaturas/` para asignar una asignatura a un usuario.
* Endpoint **GET** `/asignacion_asignaturas/{id_asignacion}` para obtener una asignación por su ID.
* Endpoint **GET** `/asignacion_asignaturas/` para listar todas las asignaciones de asignaturas.
* Integración de modelos y esquemas para la gestión de asignaciones de asignaturas.
