# Feature Specification: CRUD Persona + Usuario

**Feature Branch**: `feature/crud-persona` (Est. 2) + `feature/crud-usuario` (Est. 3)
**Created**: 2026-04-14
**Status**: Completed

## User Story 1 - CRUD Persona (Priority: P1) `[P]`

CRUD de persona (codigo, nombre, telefono, direccion). Estudiante 2.

**Acceptance Scenarios**:

1. **Given** personas en BD, **When** navego a /persona, **Then** veo tabla con datos
2. **Given** formulario lleno, **When** guardo, **Then** persona creada con flash exito

## User Story 2 - CRUD Usuario (Priority: P1) `[P]`

CRUD de usuario (email, contrasena, nombre). Estudiante 3.
La contrasena se muestra como campo password (no se ve).

**Acceptance Scenarios**:

1. **Given** usuarios en BD, **When** navego a /usuario, **Then** veo tabla (contrasena NO visible)
2. **Given** formulario con email + contrasena, **When** guardo, **Then** usuario creado
