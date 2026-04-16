# Etapa 5: Tareas y Codigo

> Segun [Spec-Kit](https://github.com/github/spec-kit): las tareas se derivan del plan y
> se organizan por historia de usuario. Cada tarea tiene ruta de archivo especifica
> y marcadores de paralelizacion `[P]`. Se generan con `/speckit.tasks`.
>
> Referencia: [tasks-template.md](https://github.com/github/spec-kit/blob/main/templates/plan-template.md)

---

## Leyenda

- `[x]` = Completado
- `[ ]` = Pendiente
- `[P]` = Paralelizable (puede hacerse al mismo tiempo que otra tarea [P])
- `->` = Dependencia (requiere que la tarea anterior este completada)

---

## Historia 1: Proyecto base (Paso 3)

**Estudiante 1 — Rama: main (commit inicial)**

- [x] Crear carpeta `FrontFlaskTutorial/`
- [x] Crear entorno virtual: `python -m venv venv`
- [x] Instalar dependencias: `pip install flask requests`
- [x] Crear `requirements.txt`: `pip freeze > requirements.txt`
- [x] Crear `config.py` con `API_BASE_URL` y `SECRET_KEY`
  - Archivo: `config.py`
- [x] Crear `app.py` con Flask y registro de blueprints
  - Archivo: `app.py`
- [x] Crear `routes/__init__.py` y `services/__init__.py`
- [x] Crear `.gitignore` (venv/, __pycache__/, *.pyc)
- [x] Inicializar git, primer commit, push a GitHub
- [x] Invitar colaboradores

---

## Historia 2: Servicio API (Paso 4)

**Estudiante 1 — Rama: api-service**

- [x] Crear `services/api_service.py` con clase `ApiService`
  - Archivo: `services/api_service.py`
  - Metodos: `listar()`, `crear()`, `actualizar()`, `eliminar()`
- [x] Verificar conexion con la API: `GET /api/producto`
- [x] Merge a main

---

## Historia 3: Layout y navegacion (Paso 5)

**Estudiante 1 — Rama: layout**

- [x] Crear `templates/layout/base.html` con Bootstrap 5 CDN
  - Sidebar + top-row + content area
- [x] Crear `templates/components/nav_menu.html` con links
- [x] Crear `templates/pages/home.html` (pagina inicio)
- [x] Crear `routes/home.py` con Blueprint
- [x] Registrar blueprint en `app.py`
- [x] Crear `static/css/app.css` con variables CSS
- [x] Merge a main

---

## Historia 4: CRUD Producto (Paso 6)

**Estudiante 1 — Rama: feature/crud-producto**

- [x] Crear `routes/producto.py` con Blueprint
  - `index()`: listar, `crear()`: POST, `editar()`: POST, `eliminar()`: GET
- [x] Crear `templates/pages/producto.html`
  - Tabla HTML + formulario crear/editar + flash messages
- [x] Registrar blueprint en `app.py`
- [x] Merge a main

---

## Historia 5: CRUD Persona + Usuario (Paso 7) `[P]`

**Estudiante 2 — Rama: feature/crud-persona**
**Estudiante 3 — Rama: feature/crud-usuario**

- [x] `[P]` Crear `routes/persona.py` + `templates/pages/persona.html` (Est. 2)
- [x] `[P]` Crear `routes/usuario.py` + `templates/pages/usuario.html` (Est. 3)
- [x] Registrar blueprints en `app.py`
- [x] Merge ambas ramas a main

---

## Historia 6: CRUD Empresa, Cliente, Rol (Paso 8) `[P]`

**Estudiante 2 — Rama: feature/crud-empresa-cliente**

- [x] `[P]` Crear `routes/empresa.py` + `templates/pages/empresa.html`
- [x] `[P]` Crear `routes/cliente.py` + `templates/pages/cliente.html`
  - Select FK para persona y empresa (cargados desde API)
- [x] `[P]` Crear `routes/rol.py` + `templates/pages/rol.html`
- [x] Merge a main

---

## Historia 7: CRUD Ruta, Vendedor, NavMenu (Paso 9) `[P]`

**Estudiante 3 — Rama: feature/crud-ruta-vendedor**

- [x] `[P]` Crear `routes/ruta.py` + `templates/pages/ruta.html`
- [x] `[P]` Crear `routes/vendedor.py` + `templates/pages/vendedor.html`
- [x] Actualizar `templates/components/nav_menu.html` con todas las tablas
- [x] Merge a main

---

## Historia 8: Factura maestro-detalle (Paso 10)

**Estudiante 2 — Rama: feature/factura**
-> Depende de: Historia 6 + Historia 7

- [x] Crear `routes/factura.py` con logica maestro-detalle
  - Cabecera: vendedor (select FK), cliente (select FK), fecha
  - Detalle: tabla dinamica con producto, cantidad, precio
- [x] Crear `templates/pages/factura.html`
  - JavaScript para agregar/eliminar filas de detalle
  - Calculo de subtotales y total
- [x] Merge a main

---

## Historia 9: Login y Control de Acceso (Paso 12)

**Estudiante 1 — Rama: feature/login**
-> Depende de: Todas las historias anteriores

### 9.1 Servicio de autenticacion
- [x] Crear `services/auth_service.py`
  - Archivo: `services/auth_service.py`
  - Descubrimiento dinamico FK/PK via `/api/estructuras/basedatos`
  - `_post_consulta()`: POST a ConsultasController
  - `obtener_roles_y_rutas()`: 1 SQL con JOINs (roles + rutas)
  - `obtener_roles_usuario()`: llama `obtener_roles_y_rutas`, cachea rutas
  - `obtener_rutas_permitidas()`: usa cache o fallback
  - Fallback: `_obtener_roles_fallback()`, `_obtener_rutas_fallback()` (5 GETs)
  - `login()`: POST `/api/autenticacion/token`
  - `actualizar_contrasena()`: PUT con `?camposEncriptar=contrasena`

### 9.2 Middleware
- [x] Crear `middleware/auth_middleware.py`
  - Archivo: `middleware/auth_middleware.py`
  - `crear_middleware(app)`: registra `before_request` + `context_processor`
  - Rutas publicas: `/login`, `/logout`, `/static`, `/recuperar-contrasena`
  - Sin sesion -> redirect `/login`
  - Ruta no permitida -> pagina 403

### 9.3 Rutas de autenticacion
- [x] Crear `routes/auth.py` con Blueprint
  - `/login` GET/POST, `/logout`, `/cambiar-contrasena`, `/recuperar-contrasena`
  - Guardar token JWT en `session["token"]`
  - Verificar roles no vacios
  - Validacion contrasena (6 chars, mayuscula, numero)

### 9.4 JWT en ApiService
- [x] Modificar `services/api_service.py`
  - Agregar `_headers()` con `Authorization: Bearer {token}`
  - Agregar `headers=self._headers()` en cada `requests.get/post/put/delete`

### 9.5 Templates de auth
- [x] `templates/pages/login.html` — formulario login
- [x] `templates/pages/cambiar_contrasena.html` — cambiar contrasena
- [x] `templates/pages/recuperar_contrasena.html` — recuperar contrasena
- [x] `templates/pages/sin_acceso.html` — pagina 403

### 9.6 Servicio email
- [x] Crear `services/email_service.py` — SMTP para contrasena temporal

### 9.7 Modificar existentes
- [x] `app.py`: agregar `crear_middleware(app)` + `auth_bp`
- [x] `templates/layout/base.html`: agregar boton login/logout en top-row
- [x] `config.py`: agregar variables SMTP

### 9.8 Documentacion
- [x] Crear `Paso12_LoginYControlDeAcceso.md` — documento completo

---

## Validacion final

- [x] Login con usuario sin roles -> "No tiene roles asignados"
- [x] Login con usuario con rol Contador -> entra, solo ve sus rutas
- [x] Login con usuario con todos los roles -> acceso total
- [x] JWT se envia en cada peticion (verificar en F12 Network)
- [x] Ruta no permitida -> pagina 403
- [x] Cambiar contrasena funciona con BCrypt
- [x] Proyecto arranca con `python app.py` sin errores

---

## Artefactos generados (resultado del SDD)

Siguiendo [Spec-Kit](https://github.com/github/spec-kit), estos son los artefactos que se produjeron:

| Artefacto SDD | Archivo en este proyecto |
|---------------|--------------------------|
| constitution.md | `sdd/01_constitucion.md` |
| spec.md | `sdd/02_especificacion.md` |
| clarify | `sdd/03_clarificacion.md` |
| plan.md | `sdd/04_plan.md` |
| tasks.md | `sdd/05_tareas.md` (ESTE archivo) |
| Codigo fuente | `app.py`, `routes/`, `services/`, `templates/`, etc. |
| Documentacion paso a paso | `Paso0.md` a `Paso12.md` |

> "Lo mas importante del SDD es que la documentacion es un entregable que se versiona,
> y el codigo es el resultado de esta documentacion."

---

## Referencias

- [GitHub Spec-Kit](https://github.com/github/spec-kit) — Toolkit oficial SDD
- [spec-driven.md](https://github.com/github/spec-kit/blob/main/spec-driven.md) — Documento tecnico SDD
- [Diving Into SDD With Spec Kit (Microsoft)](https://developer.microsoft.com/blog/spec-driven-development-spec-kit)
- [Video: La forma CORRECTA de programar con IA en 2026](https://youtu.be/p2WA672HrdI)
