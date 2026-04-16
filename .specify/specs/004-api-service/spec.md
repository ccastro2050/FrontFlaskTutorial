# Feature Specification: API Service

**Feature Branch**: `api-service`
**Created**: 2026-04-14
**Status**: Completed

## User Story 1 - Servicio generico para consumir la API REST (Priority: P1)

Crear una clase ApiService con los 4 metodos CRUD (listar, crear, actualizar, eliminar) que se reutiliza en todos los Blueprints.

**Acceptance Scenarios**:

1. **Given** la API corriendo en localhost:5035, **When** llamo `api.listar("producto")`, **Then** retorna una lista de diccionarios con los datos
2. **Given** datos validos, **When** llamo `api.crear("producto", datos)`, **Then** retorna `(True, "Registro creado")`
3. **Given** la API no esta corriendo, **When** llamo cualquier metodo, **Then** retorna lista vacia o `(False, "Error de conexion")`
