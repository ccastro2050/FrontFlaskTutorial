# Feature Specification: CRUD Empresa, Cliente, Rol

**Feature Branch**: `feature/crud-empresa-cliente`
**Created**: 2026-04-14
**Status**: Completed

## User Story 1 - CRUD Empresa (Priority: P1)

CRUD de empresa (codigo, nombre, nit, direccion).

## User Story 2 - CRUD Cliente con FK (Priority: P1)

CRUD de cliente con selects FK para persona y empresa. fkcodempresa es nullable (persona natural no tiene empresa).

**Acceptance Scenarios**:

1. **Given** personas y empresas en BD, **When** abro formulario cliente, **Then** veo selects cargados con personas y empresas
2. **Given** cliente persona natural, **When** dejo empresa vacia, **Then** se crea con fkcodempresa = null

## User Story 3 - CRUD Rol (Priority: P1)

CRUD de rol (id, nombre). Tabla de catalogo para seguridad.
