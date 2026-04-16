# Feature Specification: Login y Control de Acceso

**Feature Branch**: `feature/login`
**Created**: 2026-04-14
**Status**: Completed

## User Scenarios & Testing

### User Story 1 - Login con email y contrasena (Priority: P1)

Un usuario escribe su email y contrasena en el formulario de login. El sistema verifica las credenciales contra la API (BCrypt) y, si son correctas, carga sus roles y rutas permitidas en la sesion.

**Why this priority**: Sin login no hay acceso al sistema. Es el punto de entrada obligatorio.

**Independent Test**: Hacer POST /login con credenciales validas y verificar redirect a /.

**Acceptance Scenarios**:

1. **Given** un usuario con email "admin@test.com" y contrasena "Admin123" existe en la BD, **When** escribe esas credenciales en /login, **Then** redirige a / con mensaje "Bienvenido" y session["usuario"] = "admin@test.com"
2. **Given** un usuario con email "admin@test.com", **When** escribe contrasena incorrecta, **Then** muestra "Credenciales incorrectas" y se queda en /login
3. **Given** un email que no existe en la BD, **When** intenta login, **Then** muestra "Usuario no encontrado"

---

### User Story 2 - Control de acceso por roles y rutas (Priority: P1)

Cada usuario tiene roles asignados. Cada rol tiene rutas permitidas. El middleware verifica en CADA request si el usuario puede acceder a la ruta actual. Si no tiene permiso, muestra pagina 403.

**Why this priority**: Sin control de acceso, cualquier usuario autenticado ve todo.

**Independent Test**: Login con usuario que tiene rol "Contador" (rutas: /producto, /cliente). Navegar a /factura debe mostrar 403.

**Acceptance Scenarios**:

1. **Given** usuario con rol "Contador" que tiene rutas [/producto, /cliente], **When** navega a /producto, **Then** muestra la pagina normalmente
2. **Given** usuario con rol "Contador", **When** navega a /factura, **Then** muestra "Acceso Denegado" (403)
3. **Given** usuario sin roles asignados, **When** intenta login, **Then** muestra "El usuario no tiene roles asignados" y no entra

---

### User Story 3 - JWT en cada peticion HTTP (Priority: P1)

El token JWT obtenido al hacer login se envia automaticamente en el header Authorization de cada peticion a la API. Si la API tiene [Authorize], solo acepta peticiones con token valido.

**Why this priority**: Sin JWT, la API queda abierta a cualquiera con Postman.

**Independent Test**: Verificar en F12 -> Network que las peticiones llevan header Authorization: Bearer.

**Acceptance Scenarios**:

1. **Given** usuario logueado, **When** navega a /producto, **Then** la peticion GET /api/producto lleva header `Authorization: Bearer eyJhbG...`
2. **Given** API con [Authorize] activo, **When** un usuario NO logueado intenta GET /api/producto desde Postman sin token, **Then** responde 401 Unauthorized

---

### User Story 4 - Cambiar contrasena (Priority: P2)

El usuario puede cambiar su contrasena. Se valida: minimo 6 caracteres, al menos 1 mayuscula, al menos 1 numero. La API encripta con BCrypt antes de guardar.

**Why this priority**: Necesario para recuperacion de contrasena (flujo completo).

**Independent Test**: Login -> /cambiar-contrasena -> escribir nueva -> verificar que funciona con la nueva.

**Acceptance Scenarios**:

1. **Given** usuario logueado, **When** escribe nueva contrasena "Nuevo123" y confirma, **Then** se actualiza en BD con BCrypt y redirige a /
2. **Given** usuario, **When** escribe contrasena "abc" (menos de 6 chars), **Then** muestra "Minimo 6 caracteres"

---

### User Story 5 - Recuperar contrasena (Priority: P3)

El usuario olvido su contrasena. Ingresa su email, el sistema genera una temporal, la guarda con BCrypt, la envia por SMTP, y fuerza cambio en el siguiente login.

**Why this priority**: Funcionalidad complementaria, no bloquea el uso basico.

**Independent Test**: /recuperar-contrasena -> ingresar email -> verificar que llega correo (o se muestra temporal si SMTP no esta configurado).

**Acceptance Scenarios**:

1. **Given** email "admin@test.com" existe en BD y SMTP configurado, **When** solicita recuperar, **Then** recibe correo con contrasena temporal
2. **Given** SMTP no configurado, **When** solicita recuperar, **Then** muestra temporal en pantalla con warning

---

## Technical Notes

- Roles y rutas se cargan con 1 sola consulta SQL via ConsultasController (no 5 GETs separados)
- FKs y PKs se descubren dinamicamente via GET /api/estructuras/basedatos
- La sesion usa cookie firmada con SECRET_KEY de Flask (HMAC)
- El middleware before_request intercepta CADA request antes de llegar al Blueprint

## Dependencies

- Tablas: usuario, rol, rol_usuario, ruta, rutarol (5 tablas de seguridad)
- API: ApiGenericaCsharp corriendo en puerto 5035
- SMTP: Gmail con App Password (opcional, para recuperar contrasena)
