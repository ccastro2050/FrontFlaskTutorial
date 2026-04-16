# Feature Specification: Factura Maestro-Detalle

**Feature Branch**: `feature/factura`
**Created**: 2026-04-14
**Status**: Completed
**Dependencies**: 008-crud-empresa-cliente-rol, 009-crud-ruta-vendedor

## User Story 1 - Crear factura con cabecera y detalle (Priority: P1)

Formulario con cabecera (vendedor, cliente, fecha) y tabla dinamica de productos (agregar/eliminar filas con JavaScript). Al guardar, se crea la factura y sus productos en la API.

**Acceptance Scenarios**:

1. **Given** vendedores, clientes y productos en BD, **When** abro formulario factura, **Then** veo selects FK cargados para vendedor, cliente y producto
2. **Given** formulario con 1 cabecera y 3 lineas de detalle, **When** guardo, **Then** se crea 1 factura + 3 registros en productosporfactura
3. **Given** formulario con detalle, **When** hago clic en "Agregar producto", **Then** aparece nueva fila en la tabla de detalle (JavaScript)
4. **Given** fila de detalle, **When** hago clic en "X" (eliminar fila), **Then** la fila desaparece

## User Story 2 - Listar facturas (Priority: P1)

Ver todas las facturas con numero, fecha, vendedor, cliente, total.

**Acceptance Scenarios**:

1. **Given** facturas en BD, **When** navego a /factura, **Then** veo tabla con facturas y sus datos
