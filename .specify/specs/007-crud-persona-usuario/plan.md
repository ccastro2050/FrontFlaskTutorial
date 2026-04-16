# Implementation Plan: CRUD Persona + Usuario

**Status**: Completed

## Components

| Archivo | Estudiante | Responsabilidad |
|---------|-----------|----------------|
| `routes/persona.py` | Est. 2 | Blueprint CRUD persona |
| `templates/pages/persona.html` | Est. 2 | Tabla + formulario persona |
| `routes/usuario.py` | Est. 3 | Blueprint CRUD usuario |
| `templates/pages/usuario.html` | Est. 3 | Tabla + formulario usuario (password oculto) |

## Paralelizacion

Ambos CRUDs son independientes `[P]`. Est. 2 y Est. 3 trabajan en paralelo en ramas separadas.
