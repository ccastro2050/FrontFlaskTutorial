# Implementation Plan: Login y Control de Acceso

**Feature**: 012-login-y-control-acceso
**Created**: 2026-04-14
**Status**: Completed
**Constitution Compliance**: Verified (SOLID, ACID, 3 capas seguridad)

## Technical Summary

Implementar autenticacion completa en Flask: login con BCrypt via API, token JWT en cada peticion, control de acceso por roles/rutas con middleware, cambiar y recuperar contrasena.

## Architecture

```
Navegador -> Middleware (before_request) -> Blueprint (routes/auth.py)
                                               |
                                         AuthService -> API C# -> PostgreSQL
                                               |
                                         session Flask (cookie firmada)
```

## Components

| Componente | Archivo | Responsabilidad | Principio SOLID |
|-----------|---------|-----------------|-----------------|
| AuthService | services/auth_service.py | Login, roles, rutas, ConsultasController | S (solo auth) |
| AuthController | routes/auth.py | Rutas /login, /logout, /cambiar | S (solo rutas auth) |
| AuthMiddleware | middleware/auth_middleware.py | Interceptar requests, verificar permisos | S (solo verificar) |
| EmailService | services/email_service.py | Enviar correo SMTP | S (solo email) |
| ApiService (mod) | services/api_service.py | Agregar JWT a _headers() | O (extension sin modificar logica) |

## Data Model Changes

No se crean tablas nuevas. Se usan las 5 tablas de seguridad existentes:
- usuario (email PK, contrasena BCrypt)
- rol (id, nombre)
- rol_usuario (fkemail FK, fkidrol FK)
- ruta (id, ruta, descripcion)
- rutarol (fkidrol FK, fkidruta FK)

## API Endpoints Used

| Endpoint | Para que |
|----------|----------|
| POST /api/autenticacion/token | Login BCrypt + JWT |
| GET /api/estructuras/basedatos | Descubrir PKs/FKs |
| POST /api/consultas/ejecutarconsultaparametrizada | Roles + rutas en 1 SQL |
| PUT /api/usuario/{pk}/{val}?camposEncriptar=contrasena | Cambiar contrasena |

## Security Design

| Capa | Implementacion |
|------|---------------|
| BCrypt | API encripta con ?camposEncriptar=, verifica en /autenticacion/token |
| JWT | Capturado en login, guardado en session["token"], enviado en _headers() |
| Sesion | Cookie firmada HMAC, middleware verifica en cada request |
| Rutas | Middleware compara request.path vs session["rutas_permitidas"] |

## Rationale

- **ConsultasController** en vez de 5 GETs: eficiencia (BD filtra, no Python)
- **Middleware** en vez de decorador: protege TODAS las rutas automaticamente
- **Cookie firmada** en vez de JWT-only: Flask lo trae integrado
- **Descubrimiento dinamico**: funciona con cualquier BD sin cambiar codigo
