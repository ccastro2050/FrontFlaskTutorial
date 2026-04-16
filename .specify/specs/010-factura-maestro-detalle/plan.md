# Implementation Plan: Factura Maestro-Detalle

**Status**: Completed
**Dependencies**: Requiere que existan vendedores, clientes y productos en BD

## Components

| Archivo | Responsabilidad |
|---------|----------------|
| `routes/factura.py` | Blueprint con logica maestro-detalle |
| `templates/pages/factura.html` | Formulario con cabecera + tabla detalle dinamica (JS) |

## Arquitectura maestro-detalle

```
Cabecera (factura):
  vendedor (select FK -> vendedor)
  cliente (select FK -> cliente)
  fecha

Detalle (productosporfactura):
  producto (select FK -> producto)   x N filas
  cantidad
  precio (auto del producto)
  subtotal (calculado)

Total (calculado en JS)
```

## JavaScript necesario

- Agregar fila de detalle (clonar template row)
- Eliminar fila de detalle
- Calcular subtotales y total al cambiar cantidad
- Auto-llenar precio al seleccionar producto

## ACID aplicado

La API crea cabecera + detalles en una transaccion. Si falla un INSERT de detalle, la factura no se crea (atomicidad).
