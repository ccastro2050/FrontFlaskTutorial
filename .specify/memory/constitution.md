# FrontFlaskTutorial Constitution

## Core Principles

### I. API-First (Frontend desacoplado)
El frontend NUNCA accede a la base de datos directamente. Toda comunicacion con los datos pasa por la API REST generica en C# (ApiGenericaCsharp). El frontend solo hace llamadas HTTP (GET, POST, PUT, DELETE) a la API. Esto garantiza separacion de responsabilidades y permite cambiar el frontend sin afectar el backend.

### II. Descubrimiento Dinamico (No hardcodear)
Los nombres de columnas PK y FK NO se hardcodean en el codigo. Se descubren en tiempo de ejecucion consultando `GET /api/estructuras/basedatos`. Esto permite que el mismo codigo funcione con cualquier base de datos (PostgreSQL, SqlServer) sin importar como se llamen las columnas.

### III. Seguridad en 3 Capas (NON-NEGOTIABLE)
Tres capas de seguridad obligatorias:
- **BCrypt**: contrasenas encriptadas con hash irreversible en la BD (via `?camposEncriptar=contrasena`)
- **JWT**: token enviado en header `Authorization: Bearer {token}` en cada peticion HTTP
- **Sesion Flask**: cookie firmada con SECRET_KEY, verificada por middleware `before_request` en cada request

### IV. SOLID (Principios de Diseno)
- **S**: Cada archivo/clase tiene UNA responsabilidad (api_service solo HTTP, auth_service solo auth, cada Blueprint una tabla)
- **O**: Agregar CRUD nuevo = archivos nuevos, NO modificar existentes
- **L**: Servicios intercambiables donde se necesite un servicio HTTP
- **I**: ApiService tiene solo 4 metodos (listar, crear, actualizar, eliminar)
- **D**: Routes dependen de ApiService (abstraccion), no de requests directamente

### V. ACID (Integridad de Datos)
La base de datos PostgreSQL garantiza transacciones ACID:
- **Atomicidad**: factura maestro-detalle se crea completa o no se crea
- **Consistencia**: FKs siempre apuntan a registros existentes
- **Aislamiento**: transacciones concurrentes no se interfieren
- **Durabilidad**: datos persisten despues de COMMIT aunque se caiga el servidor

### VI. Simplicidad
Maximo complejidad inicial minima. Cada archivo tiene UNA responsabilidad. Sin abstracciones prematuras. Sin features especulativas. Si funciona con 3 lineas, no usar 30.

## Stack Tecnologico

| Capa | Tecnologia | Version |
|------|-----------|---------|
| Lenguaje | Python | 3.10+ |
| Framework | Flask | 3.x |
| Templates | Jinja2 | (incluido en Flask) |
| CSS | Bootstrap 5 | 5.3 CDN |
| HTTP Client | requests | 2.31+ |
| API Backend | ApiGenericaCsharp | .NET 9.0 |
| BD | PostgreSQL | 17 (compatible SqlServer) |

## Convenciones de Codigo

- **Archivos**: snake_case (`auth_service.py`, `api_service.py`)
- **Variables/funciones**: snake_case (`obtener_roles_usuario`)
- **Clases**: PascalCase (`ApiService`, `AuthService`)
- **Constantes**: UPPER_SNAKE (`API_BASE_URL`, `SIN_LIMITE`)
- **URLs**: minusculas-guiones (`/cambiar-contrasena`)
- **Tablas BD**: minusculas_guion_bajo (`rol_usuario`)

## Restricciones

- Prohibido acceder a la BD directamente desde Flask
- Prohibido usar ORM (SQLAlchemy, Peewee)
- Prohibido push directo a main (usar ramas feature/)
- Prohibido hardcodear URLs de la API (van en config.py)
- Prohibido hardcodear nombres de columnas FK/PK
- Prohibido guardar contrasenas en texto plano
- Prohibido instalar paquetes sin agregar a requirements.txt

## Patrones de Diseno Utilizados

| Patron | Donde |
|--------|-------|
| MVC | services/ + templates/ + routes/ |
| Blueprint | routes/*.py (modularizar por tabla) |
| Service Layer | services/api_service.py |
| Middleware/Interceptor | middleware/auth_middleware.py |
| Template Method | templates/layout/base.html (Jinja2 extends) |
| Facade | ApiService oculta complejidad HTTP |
| Cache | auth_service._fk_cache |
| Strategy (fallback) | ConsultasController o 5 GETs |

## Governance

La constitucion tiene prioridad sobre cualquier otra practica. Cambios a la constitucion requieren documentacion y aprobacion del equipo. Todo codigo generado por IA debe verificar cumplimiento con estos principios antes de aceptarse.

**Version**: 1.0 | **Ratified**: 2026-04-14 | **Last Amended**: 2026-04-14
