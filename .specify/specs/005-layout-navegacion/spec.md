# Feature Specification: Layout y Navegacion

**Feature Branch**: `layout`
**Created**: 2026-04-14
**Status**: Completed

## User Story 1 - Layout base con sidebar y contenido (Priority: P1)

Crear un layout HTML con Bootstrap 5 que tenga sidebar (menu lateral), barra superior y area de contenido. Todas las paginas heredan de este layout.

**Acceptance Scenarios**:

1. **Given** el layout creado, **When** abro http://localhost:5300, **Then** veo sidebar a la izquierda, barra arriba, contenido a la derecha
2. **Given** una pagina que extiende base.html, **When** la abro, **Then** hereda el sidebar y la barra, solo cambia el contenido

## User Story 2 - Menu de navegacion (Priority: P1)

Menu lateral con links a todas las tablas, colapsable por secciones.

**Acceptance Scenarios**:

1. **Given** el nav_menu creado, **When** hago clic en "Productos", **Then** navega a /producto
