# Implementation Plan: CRUD Empresa, Cliente, Rol

**Status**: Completed

## Components

| Archivo | Responsabilidad |
|---------|----------------|
| `routes/empresa.py` | Blueprint CRUD empresa |
| `routes/cliente.py` | Blueprint CRUD con selects FK (persona, empresa) |
| `routes/rol.py` | Blueprint CRUD rol |
| `templates/pages/empresa.html` | Tabla + formulario |
| `templates/pages/cliente.html` | Tabla + formulario con selects FK |
| `templates/pages/rol.html` | Tabla + formulario |

## Selects FK

Cliente carga personas y empresas via ApiService.listar() para llenar los selects.
El template usa `{% for p in personas %}` para generar las opciones.
