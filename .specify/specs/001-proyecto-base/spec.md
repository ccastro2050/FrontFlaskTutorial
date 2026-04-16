# Feature Specification: Proyecto Base

**Feature Branch**: `main` (commit inicial)
**Created**: 2026-04-14
**Status**: Completed

## User Story 1 - Crear proyecto Flask (Priority: P1)

El estudiante 1 (admin) crea la estructura del proyecto Flask con entorno virtual, dependencias, configuracion y control de versiones.

**Acceptance Scenarios**:

1. **Given** una carpeta vacia, **When** ejecuto `python -m venv venv` y `pip install flask requests`, **Then** se crea el entorno virtual con las dependencias
2. **Given** el proyecto creado, **When** ejecuto `python app.py`, **Then** Flask arranca en http://localhost:5300 sin errores
3. **Given** el proyecto funcionando, **When** hago `git init` y `git push`, **Then** el codigo esta en GitHub y los colaboradores pueden clonarlo
