# Constitucion del Proyecto: FrontFlaskTutorial

> Segun [Spec-Kit de GitHub](https://github.com/github/spec-kit): la constitucion actua como el
> "ADN arquitectonico del sistema", asegurando que toda implementacion generada mantenga
> consistencia, simplicidad y calidad. Es lo PRIMERO que lee la IA antes de generar codigo.
> Si la IA viola alguna de estas reglas, el codigo generado se rechaza.
>
> Referencia: [spec-driven.md - Los Nueve Articulos Constitucionales](https://github.com/github/spec-kit/blob/main/spec-driven.md)

---

## Articulo I: Stack Tecnologico

Toda implementacion DEBE usar exclusivamente estas tecnologias:

| Capa | Tecnologia | Version | Justificacion |
|------|-----------|---------|---------------|
| Lenguaje | Python | 3.10+ | Lenguaje del curso, los estudiantes ya lo conocen |
| Framework web | Flask | 3.x | Microframework sin magia, el estudiante ve cada linea |
| Templates | Jinja2 | (incluido en Flask) | Separacion clara logica/presentacion |
| CSS | Bootstrap 5 | 5.3 CDN | Sin npm ni build tools, responsive |
| API backend | ApiGenericaCsharp | .NET 9.0 | API generica, funciona con cualquier BD |
| BD | PostgreSQL | 17 | BD del curso, compatible con SqlServer |
| HTTP Client | requests | 2.31+ | Sincrono, simple, sin async |
| Control versiones | Git + GitHub | N/A | Trabajo colaborativo con ramas |

## Articulo II: Arquitectura del Sistema

### Arquitectura general: Cliente-Servidor en 3 capas

```
┌─────────────────────────────┐
│   CAPA DE PRESENTACION      │   FrontFlaskTutorial (este proyecto)
│   Flask + Jinja2 + Bootstrap│   Puerto 5300
│   routes/ + templates/      │   Responsabilidad: UI, navegacion, formularios
└─────────────┬───────────────┘
              │ HTTP (requests)
              │ Authorization: Bearer {JWT}
              v
┌─────────────────────────────┐
│   CAPA DE NEGOCIO (API)     │   ApiGenericaCsharp (.NET 9.0)
│   Controllers + Services    │   Puerto 5035
│   BCrypt, JWT, CRUD generico│   Responsabilidad: validacion, logica, seguridad
└─────────────┬───────────────┘
              │ SQL (ADO.NET)
              v
┌─────────────────────────────┐
│   CAPA DE DATOS             │   PostgreSQL 17
│   Tablas, FKs, indices      │   Puerto 5432
│   ACID transaccional        │   Responsabilidad: persistencia, integridad
└─────────────────────────────┘
```

**Principio: el frontend NUNCA accede a la BD directamente.** Todo pasa por la API REST.
Cada capa solo conoce a la inmediatamente inferior (no hay saltos).

### Arquitectura interna del frontend: MVC adaptado a Flask

```
                    ┌──────────────────────┐
                    │    MODELO (Model)     │
                    │  services/            │
                    │  api_service.py       │   Llama a la API via HTTP
                    │  auth_service.py      │   Logica de autenticacion
                    └──────────┬───────────┘
                               │
┌──────────────────┐           │           ┌──────────────────┐
│  VISTA (View)    │           │           │ CONTROLADOR      │
│  templates/      │ <─────────┼──────────>│ routes/          │
│  pages/*.html    │  renderiza│           │ producto.py      │
│  layout/base.html│           │           │ auth.py          │
└──────────────────┘           │           └──────────────────┘
                               │
                    ┌──────────┴───────────┐
                    │  MIDDLEWARE           │
                    │  middleware/          │
                    │  auth_middleware.py   │   Intercepta ANTES de cada request
                    └──────────────────────┘
```

| Componente MVC | Carpeta Flask | Responsabilidad |
|----------------|--------------|-----------------|
| Modelo | `services/` | Logica de negocio, llamadas HTTP a la API |
| Vista | `templates/` | HTML con Jinja2, presentacion al usuario |
| Controlador | `routes/` | Recibe requests, llama servicios, devuelve templates |
| Middleware | `middleware/` | Intercepta requests (auth, permisos) |

### Estructura de carpetas (no negociable)

```
app.py                       <- Punto de entrada (crea Flask, registra todo)
config.py                    <- Configuracion centralizada (URLs, claves, SMTP)
routes/                      <- Controladores (Blueprints)
services/                    <- Servicios: logica de negocio, llamadas HTTP
middleware/                  <- Middleware: intercepta requests (auth)
templates/
  layout/base.html           <- Layout base (sidebar + content)
  components/nav_menu.html   <- Menu lateral
  pages/{tabla}.html          <- Una pagina por tabla
static/css/                  <- Estilos
scripts_bds/                 <- Scripts SQL
sdd/                         <- Documentacion SDD (ESTOS archivos)
```

## Articulo III: Convenciones de Codigo

| Elemento | Convencion | Ejemplo |
|----------|-----------|---------|
| Archivos Python | snake_case | `auth_service.py`, `api_service.py` |
| Variables/funciones | snake_case | `obtener_roles_usuario()` |
| Clases | PascalCase | `ApiService`, `AuthService` |
| Constantes | UPPER_SNAKE | `API_BASE_URL`, `SIN_LIMITE` |
| Rutas URL | minusculas-guiones | `/cambiar-contrasena`, `/sin-acceso` |
| Tablas BD | minusculas_guion_bajo | `rol_usuario`, `rutarol` |
| Blueprints | nombre de la tabla | `bp = Blueprint("producto", __name__)` |
| Templates | nombre de la tabla | `templates/pages/producto.html` |

## Articulo IV: Patron CRUD

Cada tabla sigue este patron exacto (no negociable):

```python
# routes/{tabla}.py
bp = Blueprint("{tabla}", __name__)
api = ApiService()

@bp.route("/{tabla}")                    # Listar
def index(): ...

@bp.route("/{tabla}/crear", methods=["POST"])  # Crear
def crear(): ...

@bp.route("/{tabla}/editar/<id>", methods=["POST"])  # Editar
def editar(id): ...

@bp.route("/{tabla}/eliminar/<id>")      # Eliminar
def eliminar(id): ...
```

## Articulo V: Seguridad (3 capas obligatorias)

> Referencia: Paso12_LoginYControlDeAcceso.md

| Capa | Donde | Que protege | Como |
|------|-------|-------------|------|
| **BCrypt** | BD (via API) | Contrasenas | `?camposEncriptar=contrasena` |
| **JWT** | API (header HTTP) | Datos del backend | `Authorization: Bearer {token}` |
| **Sesion** | Frontend (cookie Flask) | Paginas | Middleware `before_request` |

### Middleware obligatorio
- `@app.before_request` intercepta CADA request
- Rutas publicas: `/login`, `/logout`, `/static`, `/recuperar-contrasena`
- Sin sesion -> redirect `/login`
- Ruta no permitida -> pagina 403

### Descubrimiento dinamico
- PKs y FKs se descubren via `/api/estructuras/basedatos`
- NO se hardcodean nombres de columnas
- Compatible con PostgreSQL y SqlServer

## Articulo VI: Prohibiciones

| Prohibido | Razon |
|-----------|-------|
| Acceder a la BD directamente | Todo va por la API REST |
| Usar ORM (SQLAlchemy) | No hay BD directa |
| Push directo a main | Trabajo en ramas feature/ |
| Hardcodear URLs de la API | Van en config.py |
| Hardcodear nombres FK/PK | Se descubren via API |
| Contrasenas en texto plano | BCrypt obligatorio |
| Paquetes sin requirements.txt | Rompe entorno de otros |
| JavaScript para logica de negocio | Logica en Python |

## Articulo VII: Principios SOLID

> Los principios SOLID son guias de diseno orientado a objetos que producen
> codigo mantenible, extensible y testeable. Aplican a las clases y modulos
> de este proyecto.

| Principio | Sigla | Que dice | Como se aplica en este proyecto |
|-----------|-------|----------|--------------------------------|
| **Single Responsibility** | S | Una clase tiene UNA sola razon para cambiar | `ApiService` solo hace HTTP, `AuthService` solo hace auth, cada Blueprint maneja UNA tabla |
| **Open/Closed** | O | Abierto para extension, cerrado para modificacion | Agregar un CRUD nuevo = crear archivos nuevos, NO modificar los existentes |
| **Liskov Substitution** | L | Los subtipos deben ser sustituibles por sus tipos base | `ApiService` y `AuthService` son intercambiables donde se necesite un servicio HTTP |
| **Interface Segregation** | I | No forzar a depender de interfaces que no se usan | `ApiService` tiene solo 4 metodos (listar, crear, actualizar, eliminar), no un metodo gigante |
| **Dependency Inversion** | D | Depender de abstracciones, no de implementaciones | Las rutas dependen de `ApiService` (abstraccion), no de `requests` directamente |

### Aplicacion concreta

```
CORRECTO (S - Single Responsibility):
  routes/producto.py    <- Solo maneja rutas de producto
  services/api_service.py <- Solo hace llamadas HTTP
  middleware/auth_middleware.py <- Solo verifica permisos

INCORRECTO:
  routes/producto.py que tambien hace llamadas HTTP directas
  app.py que tiene logica de negocio mezclada con registro de blueprints
```

```
CORRECTO (O - Open/Closed):
  Para agregar CRUD de "proveedor":
    1. Crear routes/proveedor.py (NUEVO)
    2. Crear templates/pages/proveedor.html (NUEVO)
    3. Registrar blueprint en app.py (1 linea)
  NO se modifica: api_service.py, auth_service.py, base.html

INCORRECTO:
  Agregar un if/elif en api_service.py para cada tabla nueva
```

## Articulo VIII: Principios ACID (Base de Datos)

> ACID son las propiedades que garantizan la integridad de las transacciones
> en la base de datos. PostgreSQL las cumple por defecto.

| Principio | Que garantiza | Ejemplo en este proyecto |
|-----------|---------------|--------------------------|
| **Atomicity** (Atomicidad) | Una transaccion se ejecuta COMPLETA o NO se ejecuta | Factura maestro-detalle: si falla un producto, no se crea la factura |
| **Consistency** (Consistencia) | La BD pasa de un estado valido a otro estado valido | Un FK `fkcodcliente` siempre apunta a un cliente que existe |
| **Isolation** (Aislamiento) | Transacciones concurrentes no se interfieren | Dos usuarios creando facturas al mismo tiempo no se pisan |
| **Durability** (Durabilidad) | Una vez confirmada, la transaccion persiste aunque se caiga el servidor | Despues de `COMMIT`, el registro existe aunque se reinicie PostgreSQL |

### Donde aplica ACID en este proyecto

```
ACID lo maneja PostgreSQL + la API (capa de datos).
El frontend (Flask) NO maneja transacciones directamente.

Frontend (Flask)          API (C#)              BD (PostgreSQL)
   POST /factura  ──>  Recibe datos  ──>  BEGIN TRANSACTION
                                          INSERT factura
                                          INSERT productos (N)
                                          COMMIT (atomico)
                                          
Si falla un INSERT ──>  ROLLBACK  ──>  Nada se guarda (atomicidad)
```

## Articulo IX: Patrones de Diseno

> Patrones de diseno utilizados en este proyecto, con referencia a donde se aplican.

| Patron | Tipo | Donde se usa | Que resuelve |
|--------|------|-------------|-------------|
| **MVC** (Model-View-Controller) | Arquitectonico | services/ + templates/ + routes/ | Separar logica, presentacion y control |
| **Blueprint** (Flask) | Estructural | routes/*.py | Modularizar rutas por funcionalidad |
| **Service Layer** | Arquitectonico | services/api_service.py | Encapsular logica de negocio en una capa |
| **Middleware/Interceptor** | Comportamiento | middleware/auth_middleware.py | Ejecutar logica ANTES de cada request |
| **Template Method** | Comportamiento | templates/layout/base.html | Layout comun, cada pagina llena los bloques |
| **Facade** | Estructural | services/api_service.py | Interfaz simple para la API REST compleja |
| **Cache** | Rendimiento | auth_service._fk_cache | No repetir consultas a la API |
| **Strategy (fallback)** | Comportamiento | auth_service: ConsultasController o 5 GETs | Cambiar estrategia segun disponibilidad |

### Ejemplo: Patron Template Method en Jinja2

```html
<!-- base.html (template padre) -->
<div class="sidebar">{% include 'components/nav_menu.html' %}</div>
<div class="content">{% block content %}{% endblock %}</div>

<!-- producto.html (template hijo) -->
{% extends 'layout/base.html' %}
{% block content %}
  <!-- Solo el contenido especifico de producto -->
  <table>...</table>
{% endblock %}
```

### Ejemplo: Patron Facade en ApiService

```python
# El usuario de ApiService no necesita saber de HTTP, headers, JSON, etc.
# Solo llama metodos simples:

api = ApiService()
datos = api.listar("producto")           # Facade oculta: GET + headers + JSON parse
ok, msg = api.crear("producto", {...})    # Facade oculta: POST + headers + response check
```

## Articulo X: Simplicidad

> Segun Spec-Kit Articulo VII: "Maximo complejidad inicial minima."

- Cada archivo tiene UNA responsabilidad (SOLID - S)
- Cada ruta tiene UN blueprint
- Cada servicio tiene UNA clase
- Sin abstracciones prematuras
- Sin features especulativas

## Articulo VIII: API REST

### Endpoints permitidos

| Metodo | Endpoint | Para que |
|--------|----------|----------|
| GET | `/api/{tabla}?limite=N` | Listar |
| POST | `/api/{tabla}` | Crear |
| PUT | `/api/{tabla}/{pk}/{valor}` | Actualizar |
| DELETE | `/api/{tabla}/{pk}/{valor}` | Eliminar |
| POST | `/api/autenticacion/token` | Login BCrypt+JWT |
| GET | `/api/estructuras/basedatos` | Descubrir PKs/FKs |
| POST | `/api/consultas/ejecutarconsultaparametrizada` | SQL con JOINs |

## Articulo IX: Trabajo Colaborativo

| Regla | Detalle |
|-------|---------|
| Estrategia | GitHub Flow: main estable, feature/ para trabajo |
| Merge | Terminal: `git fetch` + `git merge`, nunca push directo |
| Commits | Descriptivos: `feat: CRUD producto`, `fix: error select` |
| Roles | Est.1 (admin), Est.2 y 3 (desarrolladores) |
| Dependencias | Solo `flask` y `requests` sin aprobacion |

---

## Fecha de ratificacion

- **Version**: 1.0
- **Fecha**: 2026-04-14
- **Autores**: Carlos Castro (profesor), Estudiantes Diseno de Software USB
- **Referencia Spec-Kit**: [github.com/github/spec-kit](https://github.com/github/spec-kit)
