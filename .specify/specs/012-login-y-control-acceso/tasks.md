# Tasks: Login y Control de Acceso

**Feature**: 012-login-y-control-acceso
**Created**: 2026-04-14
**Status**: All completed

## Task Breakdown

### Story 1: Login (P1)

- [x] Create `services/auth_service.py` with AuthService class
  - [x] `_obtener_estructura()`, `_obtener_fk()`, `_obtener_pk()` (dynamic discovery)
  - [x] `_post_consulta()` (ConsultasController)
  - [x] `login()` (POST /api/autenticacion/token)
  - [x] `obtener_roles_y_rutas()` (1 SQL with JOINs)
  - [x] `obtener_roles_usuario()` (calls obtener_roles_y_rutas, caches rutas)
  - [x] `obtener_rutas_permitidas()` (uses cache or fallback)
  - [x] `_obtener_roles_fallback()`, `_obtener_rutas_fallback()` (5 GETs)
- [x] Create `routes/auth.py` with Blueprint
  - [x] GET/POST `/login`
  - [x] GET `/logout`
  - [x] Store JWT in session: `session["token"] = data["token"]`
- [x] Create `templates/pages/login.html`
- [x] Register blueprint in `app.py`

### Story 2: Control de acceso (P1)

- [x] Create `middleware/auth_middleware.py`
  - [x] `crear_middleware(app)` with `@app.before_request`
  - [x] Public routes: /login, /logout, /static, /recuperar-contrasena
  - [x] No session -> redirect /login
  - [x] Route not in rutas_permitidas -> render sin_acceso.html, 403
  - [x] context_processor: inject usuario, roles, rutas_permitidas
- [x] Create `templates/pages/sin_acceso.html`
- [x] Register middleware in `app.py` BEFORE blueprints

### Story 3: JWT in every request (P1) `[P]`

- [x] `[P]` Modify `services/api_service.py`
  - [x] Add `from flask import session as flask_session`
  - [x] Add `_headers()` method reading session["token"]
  - [x] Add `headers=self._headers()` to every requests call

### Story 4: Cambiar contrasena (P2)

- [x] Add `actualizar_contrasena()` to AuthService
- [x] Add GET/POST `/cambiar-contrasena` to routes/auth.py
- [x] Create `templates/pages/cambiar_contrasena.html`
- [x] Validation: 6 chars min, 1 uppercase, 1 number

### Story 5: Recuperar contrasena (P3)

- [x] Create `services/email_service.py` (SMTP)
- [x] Add GET/POST `/recuperar-contrasena` to routes/auth.py
- [x] Create `templates/pages/recuperar_contrasena.html`
- [x] Generate temp password, save with BCrypt, send via SMTP
- [x] Add SMTP config to `config.py`

### Integration

- [x] Modify `templates/layout/base.html`: add login/logout button in top-row
- [x] Create `Paso12_LoginYControlDeAcceso.md` documentation
- [x] Create `sdd/` folder with SDD documentation

## Validation

- [x] sinroles@test.com -> "No tiene roles asignados"
- [x] estudiante@test.com (Contador) -> /cliente OK, /factura 403
- [x] carlos.castro@usbmed.edu.co (all roles) -> full access
- [x] JWT in F12 Network headers
- [x] Cambiar contrasena with BCrypt
