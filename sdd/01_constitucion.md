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

## Articulo II: Arquitectura

```
FrontFlaskTutorial/          <- Frontend (este proyecto)
    |
    | HTTP (requests)
    v
ApiGenericaCsharp/           <- Backend API REST (otro proyecto)
    |
    | SQL
    v
PostgreSQL                   <- Base de datos
```

**Principio: el frontend NUNCA accede a la BD directamente.** Todo pasa por la API REST.

### Estructura de carpetas (no negociable)

```
app.py                       <- Punto de entrada
config.py                    <- Configuracion centralizada
routes/                      <- Controladores (Blueprints)
services/                    <- Logica de negocio, llamadas HTTP
middleware/                  <- Intercepta requests (auth)
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

## Articulo VII: Simplicidad

> Segun Spec-Kit Articulo VII: "Maximo complejidad inicial minima."

- Cada archivo tiene UNA responsabilidad
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
