# Feature Specification: CRUD Producto

**Feature Branch**: `feature/crud-producto`
**Created**: 2026-04-14
**Status**: Completed

## User Story 1 - Listar, crear, editar, eliminar productos (Priority: P1)

CRUD completo de la tabla producto con formulario HTML, tabla de datos, y mensajes flash.

**Acceptance Scenarios**:

1. **Given** productos existen en la BD, **When** navego a /producto, **Then** veo tabla con todos los productos
2. **Given** formulario lleno, **When** hago clic en "Guardar", **Then** se crea el producto y muestra flash "Registro creado"
3. **Given** un producto existente, **When** hago clic en "Editar", **Then** el formulario se llena con los datos actuales
4. **Given** un producto, **When** hago clic en "Eliminar", **Then** se elimina y muestra flash "Registro eliminado"
