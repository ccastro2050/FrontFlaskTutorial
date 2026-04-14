# Paso 12: Login y Control de Acceso - Flask

## Los 3 conceptos clave de seguridad

1. **Autenticacion** → ¿Quien eres? (login con email + contrasena, BCrypt verifica, JWT como credencial)
2. **Autorizacion** → ¿Que puedes hacer? (roles asignados al usuario, rutas permitidas por rol, verificacion en cada request con middleware)
3. **Encriptacion** → ¿Como se protege la informacion? (BCrypt para contrasenas en BD, SECRET_KEY para sesion en cookie, JWT firmado para peticiones a la API, HTTPS para datos en transito)

## Que se implemento

- **Login** con email y contrasena verificada con BCrypt (hash irreversible)
- **JWT** (JSON Web Token): token generado al hacer login, enviado en cada peticion a la API como header `Authorization: Bearer ...`
- **Control de acceso por roles**: cada usuario tiene roles, cada rol tiene rutas permitidas, se verifica en CADA request (middleware `before_request`)
- **Verificacion de rutas**: el middleware intercepta cada request y compara contra `rutas_permitidas` en la sesion — si no tiene permiso, muestra pagina 403
- **Cambio de contrasena** con validacion de seguridad (minimo 6 caracteres, al menos 1 mayuscula, al menos 1 numero)
- **Recuperar contrasena** genera temporal aleatoria, la guarda con BCrypt, la envia por correo SMTP (Gmail), y fuerza cambio en el siguiente login
- **Sesion persistente** con cookie firmada (encriptada con SECRET_KEY de Flask, sobrevive F5 y navegacion, se pierde al cerrar navegador)
- **Descubrimiento dinamico** de PKs y FKs via `GET /api/estructuras/{tabla}/modelo` (compatible Postgres y SqlServer, sin hardcodear nombres de columnas)
- **ConsultasController**: los roles y rutas del usuario se cargan con UNA sola consulta SQL (JOINs de 5 tablas) en vez de 5 GETs separados al CRUD generico
- **3 capas de seguridad**: BCrypt protege la BD, JWT protege la API, Sesion protege el frontend
- **[Authorize]** en la API: si se agrega este atributo en los controllers, la API rechaza peticiones sin token JWT valido

---

## Que se crea, que se modifica, que se agrega

### Archivos que se CREAN (nuevos)

| Archivo | Para que | Conceptos que usa |
|---------|---------|-------------------|
| `services/auth_service.py` | Toda la logica: login (BCrypt via API), capturar token JWT, cargar roles y rutas con ConsultasController, cambiar contrasena, descubrimiento dinamico de PKs/FKs | Autenticacion + Autorizacion + Encriptacion |
| `services/email_service.py` | Envio de correos SMTP (contrasena temporal) | Encriptacion + SMTP |
| `routes/auth.py` | Rutas: /login, /logout, /cambiar-contrasena, /recuperar-contrasena | Autenticacion |
| `middleware/auth_middleware.py` | Intercepta CADA request con `@app.before_request` y verifica si el usuario puede acceder a la ruta | Autorizacion |
| `templates/pages/login.html` | Formulario de login (email + contrasena). Sin sidebar | Autenticacion |
| `templates/pages/cambiar_contrasena.html` | Formulario para cambiar contrasena con validacion (6 chars, mayuscula, numero). Se fuerza despues de recuperar | Encriptacion (BCrypt) |
| `templates/pages/recuperar_contrasena.html` | Genera contrasena temporal, la guarda con BCrypt, la envia por SMTP | Encriptacion + SMTP |
| `templates/pages/sin_acceso.html` | Pagina error 403: "No tiene permisos". Aparece cuando el middleware detecta ruta no permitida | Autorizacion |

### Archivos que se MODIFICAN (ya existian)

| Archivo | Que se agrega | Para que |
|---------|---------------|---------|
| `config.py` | Variables SMTP (Host, Port, User, Pass, From) | Configurar correo Gmail para recuperar contrasena |
| `app.py` | `crear_middleware(app)` + `auth_bp` | Registrar el middleware de auth y las rutas de login |
| `templates/layout/base.html` | Boton login/logout en barra superior | Mostrar nombre del usuario y boton para cerrar sesion |
| `services/api_service.py` | Metodo `_headers()` que agrega header `Authorization: Bearer {token}` | Enviar JWT en cada peticion para que la API acepte las operaciones si tiene [Authorize] |

### Tablas que se necesitan en la BD (5)

| Tabla | Para que | Relacion |
|-------|---------|----------|
| `usuario` | Almacenar credenciales (email como PK + contrasena como hash BCrypt) | Tabla principal |
| `rol` | Definir tipos de usuario (Administrador, Vendedor, Contador, etc) | Tabla de catalogo |
| `rol_usuario` | Asignar roles a usuarios. Un usuario puede tener VARIOS roles | Tabla intermedia N:M entre usuario y rol |
| `ruta` | Registrar las paginas del sistema (/producto, /cliente, etc) | Tabla de catalogo |
| `rutarol` | Definir que paginas puede acceder cada rol | Tabla intermedia N:M entre rol y ruta |

---

## SQL para crear las tablas

Si las tablas no existen en la BD, ejecute este SQL:

```sql
CREATE TABLE usuario (
    email VARCHAR(200) PRIMARY KEY,
    contrasena VARCHAR(200) NOT NULL,
    nombre VARCHAR(200) DEFAULT '',
    debe_cambiar_contrasena BOOLEAN DEFAULT false
);

CREATE TABLE rol (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL
);

CREATE TABLE rol_usuario (
    id SERIAL PRIMARY KEY,
    fkemail VARCHAR(200) REFERENCES usuario(email),
    fkidrol INTEGER REFERENCES rol(id)
);

CREATE TABLE ruta (
    id SERIAL PRIMARY KEY,
    ruta VARCHAR(200) NOT NULL,
    descripcion TEXT DEFAULT ''
);

CREATE TABLE rutarol (
    id SERIAL PRIMARY KEY,
    fkidrol INTEGER REFERENCES rol(id),
    fkidruta INTEGER REFERENCES ruta(id)
);
```

---

## Diferencias con Blazor

| Aspecto | Flask | Blazor |
|---------|-------|--------|
| Sesion | Cookie firmada con SECRET_KEY (server-side) | ProtectedSessionStorage con Data Protection (browser-side) |
| Middleware | `@app.before_request` se ejecuta ANTES de cada request HTTP | `OnAfterRenderAsync` + `LocationChanged` verifican en cada navegacion |
| JWT | Se guarda en sesion Y se envia en header Authorization | Se guarda en ProtectedSessionStorage Y se envia en header Authorization |
| Templates | Jinja2 (HTML con `{{ }}` y `{% %}`) | Razor components (HTML con `@`) |
| Interactividad | POST forms + redirect + JavaScript | SignalR (todo en C# sin JS, sin recargar pagina) |
| Layout login | Template sin `{% extends base.html %}` o base sin sidebar | `@layout EmptyLayout` (sin sidebar) |
| Verificacion acceso | `before_request` compara ruta vs `rutas_permitidas` en cada request | `TieneAcceso()` compara ruta vs `RutasPermitidas` en cada navegacion |
| Pagina 403 | `render_template("sin_acceso.html"), 403` (HTTP 403) | `/sin-acceso` via `NavigateTo` (redirect client-side) |
| Variables en templates | `context_processor` inyecta usuario, roles, rutas en TODAS las templates | `@inject AuthService` en cada componente Razor |

---

## Flujo de autenticacion (paso a paso con diagrama)

```
1. El usuario ABRE http://localhost:5300 en el navegador.
         |
         v
2. Flask EJECUTA el middleware (before_request).
         |
         +-- VERIFICA si hay sesion: session.get("usuario")
         |     |
         |     +-- SI HAY sesion:
         |     |     VERIFICA si la ruta esta en rutas_permitidas.
         |     |     SI esta -> MUESTRA la pagina.
         |     |     NO esta -> MUESTRA pagina 403 "Acceso Denegado".
         |     |
         |     +-- NO HAY sesion:
         |           REDIRIGE a /login automaticamente.
         |
         v
3. Flask MUESTRA login.html (formulario de login).
         |
         +-- El usuario ESCRIBE su email y contrasena.
         |
         +-- HACE CLIC en "Iniciar sesion" -> POST /login
         |     |
         |     v
         |   SE LLAMA auth_service.login(email, contrasena):
         |     |
         |     +-- PASO 1 (estructura + autenticacion):
         |     |     |
         |     |     +-- GET /api/estructuras/usuario/modelo
         |     |     |   DESCUBRE la PK de la tabla usuario (ej: "email").
         |     |     |
         |     |     +-- POST /api/autenticacion/token
         |     |           ENVIA las credenciales a la API C#.
         |     |           La API BUSCA el usuario en la BD.
         |     |           La API COMPARA la contrasena con BCrypt (hash irreversible).
         |     |           Si COINCIDE -> GENERA un token JWT y lo DEVUELVE.
         |     |           Si NO coincide -> RECHAZA con error 401.
         |     |
         |     +-- PASO 2 (UNA sola llamada — ConsultasController):
         |     |     |
         |     |     +-- POST /api/consultas/ejecutarconsultaparametrizada
         |     |     |   ARMA una consulta SQL con JOINs usando los FK/PK descubiertos:
         |     |     |
         |     |     |   SELECT r.nombre AS nombre_rol, ruta_t.ruta
         |     |     |   FROM usuario u
         |     |     |   JOIN rol_usuario rolu ON u.email = rolu.fkemail
         |     |     |   JOIN rol r ON rolu.fkidrol = r.id
         |     |     |   JOIN rutarol rr ON r.id = rr.fkidrol
         |     |     |   JOIN ruta ruta_t ON rr.fkidruta = ruta_t.id
         |     |     |   WHERE u.email = @email
         |     |     |
         |     |     |   La BD hace el JOIN y el filtro. Solo viajan las filas
         |     |     |   de ESTE usuario (no tablas completas).
         |     |     |
         |     |     +-- Del resultado EXTRAE:
         |     |           Roles unicos: ["Administrador", "Contador", ...]
         |     |           Rutas unicas: ["/producto", "/cliente", ...]
         |     |
         |     +-- PASO 3:
         |           |
         |           +-- GUARDA en session de Flask (cookie firmada con SECRET_KEY):
         |                 session["usuario"] = "admin@correo.com"
         |                 session["token"] = "eyJhbGciOiJIUzI1NiIs..."  (JWT para la API)
         |                 session["roles"] = ["Administrador", "Contador"]
         |                 session["rutas_permitidas"] = ["/producto", "/cliente", ...]
         |
         v
4. REDIRIGE a / (pagina de inicio).
   Middleware SE EJECUTA de nuevo.
   Encuentra session["usuario"] -> permite acceso.
   MUESTRA la pagina con el sidebar, el nombre del usuario y el boton logout.
   A partir de ahora, cada peticion a la API ENVIA el token JWT en el header.
```

### Lectura del flujo (narrativa)

> Cuando el usuario abre la aplicacion en el navegador, Flask recibe el request
> y lo primero que ejecuta es el middleware (`before_request`). El middleware
> revisa si hay sesion activa leyendo `session["usuario"]`. Si encuentra una
> sesion (porque el usuario ya habia hecho login), verifica si tiene permiso
> para la ruta actual y muestra la pagina o la deniega.
>
> Si no encuentra sesion, redirige automaticamente a la pagina de login.
> El usuario escribe su email y contrasena y hace clic en "Iniciar sesion".
>
> En ese momento, el sistema descubre la estructura de la BD (para saber como
> se llaman las columnas sin hardcodearlas) y envia las credenciales a la API.
>
> La API recibe el email y la contrasena en texto plano, busca al usuario en la
> base de datos, y compara la contrasena con el hash BCrypt guardado. Si coincide,
> genera un token JWT (una credencial temporal con expiracion) y lo devuelve.
> Si no coincide, rechaza con un error.
>
> Con el login exitoso, el sistema usa los nombres de FK y PK que descubrio
> de la estructura para armar UNA sola consulta SQL con JOINs de 5 tablas.
> Esta consulta se envia a ConsultasController, que la ejecuta en la base de datos
> y devuelve solo las filas que pertenecen a este usuario. Del resultado se
> extraen los roles unicos (Administrador, Contador, etc.) y las rutas unicas
> (/producto, /cliente, etc.) que el usuario puede acceder.
>
> Toda esta informacion (usuario, token, roles, rutas) se guarda en la sesion
> de Flask. La sesion es una cookie firmada con SECRET_KEY — el usuario no puede
> manipularla porque si cambia un byte, la firma no coincide y Flask la invalida.
>
> Finalmente, redirige a la pagina de inicio. A partir de ese momento, cada vez
> que el usuario visita una pagina, el middleware se ejecuta ANTES de procesar
> el request: verifica que tenga sesion y que la ruta este en sus rutas_permitidas.
> Si la ruta esta en la lista, muestra la pagina. Si no esta, muestra la pagina
> "Acceso Denegado" (403).
>
> Al mismo tiempo, cada vez que se hace una peticion a la API (listar registros,
> crear, actualizar o eliminar), el token JWT se envia automaticamente en el
> header Authorization de la peticion HTTP. Si la API tiene [Authorize] en sus
> controllers, verifica que el token sea valido y no haya expirado. Si el token
> es valido, permite la operacion. Si no lo es, responde 401 Unauthorized.
>
> Cuando el usuario hace clic en "Cerrar sesion", el sistema limpia toda la
> sesion de Flask y redirige a la pagina de login. Si el usuario intenta navegar
> a cualquier pagina despues de cerrar sesion, el middleware detecta que no hay
> sesion y lo redirige al login de nuevo.

## Como funciona la proteccion de rutas

La proteccion de rutas se ejecuta en CADA request gracias al middleware `before_request`.

### El middleware (auth_middleware.py)

```python
# Se ejecuta ANTES de cada request HTTP

@app.before_request
def verificar_autenticacion():
    # 1. Rutas publicas: /login, /static, etc -> dejar pasar siempre
    if any(request.path.startswith(r) for r in RUTAS_PUBLICAS):
        return

    # 2. No hay sesion? -> redirigir a /login
    if not session.get("usuario"):
        return redirect(url_for("auth.login"))

    # 3. Debe cambiar contrasena? -> forzar cambio
    if session.get("debe_cambiar_contrasena") and request.path != "/cambiar-contrasena":
        return redirect(url_for("auth.cambiar_contrasena"))

    # 4. Home siempre accesible
    if request.path == "/":
        return

    # 5. Sin rutas configuradas -> permitir todo (sistema nuevo)
    rutas_permitidas = set(session.get("rutas_permitidas", []))
    if not rutas_permitidas:
        return

    # 6. Verificar si la ruta esta permitida (exacta o sub-ruta)
    ruta_actual = request.path
    for ruta in rutas_permitidas:
        if ruta_actual == ruta or ruta_actual.startswith(ruta + "/"):
            return  # Permitido

    # 7. No permitida -> 403
    return render_template("pages/sin_acceso.html"), 403
```

### Diferencia con Blazor

| Aspecto | Flask (middleware) | Blazor (MainLayout) |
|---------|-------------------|---------------------|
| Cuando se ejecuta | ANTES de cada request HTTP | Despues del primer render + en cada navegacion |
| Como se implementa | `@app.before_request` | `OnAfterRenderAsync` + `LocationChanged` |
| Que retorna si no tiene permiso | `render_template("sin_acceso.html"), 403` | `NavigateTo("/sin-acceso")` |
| Automatico | Si, intercepta TODO | Si, pero necesita `IDisposable` para limpiar el listener |

### Ejemplo de funcionamiento

```
rutas_permitidas = ["/producto", "/cliente", "/home"]

GET /producto          -> middleware verifica -> esta en la lista -> PERMITE
GET /producto/crear    -> middleware verifica -> sub-ruta de /producto -> PERMITE
GET /factura           -> middleware verifica -> NO esta en la lista -> 403
GET /                  -> middleware verifica -> home siempre accesible -> PERMITE
```

Si `rutas_permitidas` esta vacio (sistema nuevo sin configurar), permite todo
para no bloquear al primer usuario.

### El context_processor

El `context_processor` inyecta las variables de sesion en TODAS las templates
Jinja2 automaticamente. Asi no hay que pasarlas en cada `render_template()`:

```python
@app.context_processor
def inyectar_sesion():
    return {
        "usuario": session.get("usuario", ""),
        "nombre_usuario": session.get("nombre_usuario", ""),
        "roles": session.get("roles", []),
        "rutas_permitidas": set(session.get("rutas_permitidas", [])),
    }
```

En cualquier template Jinja2:
```html
<!-- Mostrar nombre del usuario -->
<span>{{ nombre_usuario }}</span>

<!-- Mostrar/ocultar enlace segun permisos -->
{% if "/producto" in rutas_permitidas %}
    <a href="/producto">Productos</a>
{% endif %}
```

---

## JWT: que es, para que y como se usa

### Que es JWT?

JWT (JSON Web Token) es un token que la API genera al hacer login exitoso.
Es un string largo con 3 partes separadas por puntos: Header.Payload.Signature

```
eyJhbGciOiJIUzI1NiIs...   <-- se ve asi en session["token"]
```

### Que es un header HTTP?

Cada peticion HTTP (GET, POST, PUT, DELETE) tiene dos partes:
- **Headers**: informacion SOBRE la peticion (quien la hace, que formato, credenciales)
- **Body**: los datos que se envian (ej: el JSON con los campos a crear)

Es como enviar una carta:
- El **header** es el sobre (remitente, destinatario, tipo de envio)
- El **body** es la carta adentro (el contenido)

El header `Authorization` es donde se pone el token JWT:

```
Ejemplo de una peticion HTTP completa:

GET /api/producto HTTP/1.1          <-- metodo + ruta
Host: localhost:5035                <-- header: a donde va
Content-Type: application/json      <-- header: formato de datos
Authorization: Bearer eyJhbG...     <-- header: credencial JWT

(body vacio en GET, con datos en POST/PUT)
```

Se puede ver en F12 -> Network -> clic en una peticion -> Headers.

### Para que sirve el JWT?

Si la API tiene `[Authorize]` en un controller, SOLO acepta peticiones
que traigan el token en el header Authorization:

```
GET /api/producto HTTP/1.1
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

Sin ese header -> la API responde 401 Unauthorized (rechaza la peticion).

### Como funciona en este proyecto?

```
1. Login: POST /api/autenticacion/token
   -> API verifica BCrypt -> genera JWT -> devuelve en respuesta

2. routes/auth.py captura el token:
   -> session["token"] = datos.get("token", "")
   -> Se guarda en la cookie de sesion de Flask

3. Cada peticion de ApiService:
   -> _headers() lee session["token"]
   -> Agrega: Authorization: Bearer eyJhbG...
   -> GET /api/producto  (con el JWT en el header)

4. API recibe el header:
   -> Verifica firma JWT con clave secreta
   -> Valido y no expiro -> permite la operacion
   -> Invalido o expiro -> 401 Unauthorized
```

### Como se envia el JWT en Flask (api_service.py)

```python
# En api_service.py:

def _headers(self):
    """Arma headers HTTP. Si hay token JWT, lo agrega."""
    h = {"Content-Type": "application/json"}
    token = flask_session.get("token")
    if token:
        h["Authorization"] = f"Bearer {token}"
    return h

# Cada metodo CRUD lo usa:
def listar(self, tabla, limite=None):
    respuesta = requests.get(url, params=params, headers=self._headers())
    #                                              ^^^^^^^^^^^^^^^^^^
    #                                              Envia el JWT automaticamente

def crear(self, tabla, datos):
    respuesta = requests.post(url, json=datos, headers=self._headers())

def actualizar(self, tabla, nombre_clave, valor_clave, datos):
    respuesta = requests.put(url, json=datos, headers=self._headers())

def eliminar(self, tabla, nombre_clave, valor_clave):
    respuesta = requests.delete(url, headers=self._headers())
```

### Donde esta la clave secreta?

En la API C# (`appsettings.json`):
```json
"Jwt": {
    "Key": "MySuperSecretKey1234567890...",
    "DuracionMinutos": 60
}
```
El frontend NUNCA conoce la clave. Solo la API puede generar y verificar tokens.

### JWT vs Sesion: que protege que?

| Concepto | Donde se verifica | Que protege |
|----------|------------------|-------------|
| Sesion (cookie Flask) | Frontend (middleware before_request) | Acceso a las PAGINAS |
| JWT (Authorization header) | Backend (API C#) | Acceso a los DATOS |

Ambos son necesarios:
- Sin sesion -> middleware redirige a login (no puede navegar)
- Sin JWT -> usuario ve la pagina pero no puede cargar datos (401)
- Con ambos -> usuario ve la pagina Y puede operar con datos

### Que valor agrega JWT? Por que es necesario?

Sin JWT, la API esta **completamente abierta**. Cualquier persona que conozca
la URL puede consumirla directamente desde Postman, curl o su propio codigo:

```
SIN JWT (API abierta - INSEGURO):

  Cualquiera con Postman:
    GET http://localhost:5035/api/usuario
    -> Ve TODOS los usuarios con sus hashes BCrypt

    DELETE http://localhost:5035/api/usuario/email/admin@mail.com
    -> Borra al administrador

  La sesion de Flask NO protege esto — solo protege las paginas del frontend.
  La API sigue abierta aunque el usuario no haya hecho login en Flask.
```

```
CON JWT (API protegida - SEGURO):

  Postman sin token:
    GET http://localhost:5035/api/usuario
    -> 401 Unauthorized (no puede ver nada)

  Postman CON token (obtenido via login):
    GET http://localhost:5035/api/usuario
    Headers: Authorization: Bearer eyJhbG...
    -> 200 OK (datos devueltos)

  Solo quien hizo login y tiene un token valido puede operar.
```

**Resumen**:

| Capa | Que protege | De quien |
|------|------------|----------|
| **Sesion** (Flask) | Las PAGINAS del frontend | Usuarios no logueados en el navegador |
| **JWT** (API) | Los DATOS del backend | Cualquiera que intente consumir la API directamente |
| **BCrypt** (BD) | Las CONTRASENAS en la base de datos | Alguien que acceda a la BD directamente |

Las 3 capas juntas forman la seguridad completa:
- BCrypt protege la BD (si la hackean, no ven contrasenas)
- JWT protege la API (si conocen la URL, no pueden operar sin token)
- Sesion protege el frontend (si abren el navegador, no ven paginas sin login)

### IMPORTANTE: JWT solo protege si el controller tiene [Authorize]

El JWT existe y se envia, pero **solo funciona** si el controller de la API C#
tiene el atributo `[Authorize]`. Si no lo tiene, el endpoint queda abierto
aunque el token exista.

```
Actualmente en la API generica:

  [ApiController]                        <-- NO tiene [Authorize]
  [Route("api/[controller]")]
  public class EntidadesController       <-- ABIERTO (cualquiera puede consumir)

Para proteger:

  [Authorize]                            <-- AGREGAR ESTA LINEA
  [ApiController]
  [Route("api/[controller]")]
  public class EntidadesController       <-- PROTEGIDO (requiere JWT)
```

### Donde se pone [Authorize] en la API C#?

En los controllers de la API generica. Los archivos estan en:
```
ApiGenericaCsharp/Controllers/
  EntidadesController.cs          <-- CRUD generico (listar, crear, actualizar, eliminar)
  AutenticacionController.cs      <-- Login (este NO debe tener [Authorize])
  EstructurasController.cs        <-- Estructura BD (tiene [AllowAnonymous])
  ConsultasController.cs          <-- Consultas SQL (se usa para cargar roles y rutas del login)
```

---

## Que es BCrypt

BCrypt es un algoritmo de encriptacion de contrasenas **irreversible**.

**Sin BCrypt**: `contrasena = "MiClave123"` (texto plano, inseguro)
**Con BCrypt**: `contrasena = "$2a$12$LJ3m4ys1Z..."` (hash, imposible revertir)

La API generica C# maneja BCrypt automaticamente:
- Al crear/actualizar con `?camposEncriptar=contrasena`, encripta con BCrypt
- Al autenticar con `/api/autenticacion/token`, verifica con BCrypt

---

## Sesion de Flask: que es y como funciona

### Que es la sesion de Flask?

Es un diccionario (`session`) que se guarda como cookie firmada en el navegador.
Flask firma la cookie con `SECRET_KEY` para que el usuario no pueda manipularla.

```python
# Guardar
session["usuario"] = "admin@correo.com"
session["token"] = "eyJhbGciOiJIUzI1NiIs..."
session["roles"] = ["Administrador", "Contador"]
session["rutas_permitidas"] = ["/producto", "/cliente"]

# Leer
email = session.get("usuario")
token = session.get("token")

# Borrar
session.clear()
```

### Como llegan los datos ahi?

```
routes/auth.py login_post() (despues de verificar BCrypt)
        |
        v
session["usuario"] = email
session["nombre_usuario"] = datos_usuario.get("nombre", email)
session["token"] = datos.get("token", "")
session["roles"] = roles
session["rutas_permitidas"] = list(rutas_permitidas)
        |
        v
Flask internamente:
  1. Toma el diccionario session
  2. Lo serializa a JSON
  3. Lo firma con SECRET_KEY (HMAC)
  4. Lo envia como cookie: Set-Cookie: session=eyJ...
  5. El navegador guarda la cookie
```

### Como se lee de vuelta?

```
Al visitar cualquier pagina:

  Navegador envia: Cookie: session=eyJ...
        |
        v
  Flask recibe la cookie
        +-- Verifica la firma HMAC con SECRET_KEY
        +-- Si la firma es valida -> deserializa el JSON
        +-- session["usuario"] = "admin@correo.com"
        +-- Middleware puede leerlo normalmente
```

### Por que es segura la cookie de Flask?

| Aspecto | Cookie normal | Cookie firmada (Flask) |
|---------|--------------|----------------------|
| Valores | Texto plano | Firmados con HMAC |
| Manipulable | Si (F12 -> editar) | No (si lo cambian, la firma no coincide) |
| Seguridad | Baja | Alta (requiere conocer SECRET_KEY) |

Si alguien abre F12, puede ver la cookie pero no puede descifrarla ni modificarla.
Si cambia un byte, Flask detecta que la firma no coincide y la invalida.

### Sesion Flask vs ProtectedSessionStorage (Blazor)

| | Sesion Flask | ProtectedSessionStorage |
|--|-------------|------------------------|
| Donde se guarda | Cookie del navegador | Session Storage del navegador |
| Encriptacion | Firmada con HMAC (SECRET_KEY) | Encriptada con Data Protection API |
| Persiste F5 | Si | Si |
| Persiste cerrar tab | Depende de la config | No (se borra) |
| Persiste cerrar navegador | No (cookie de sesion) | No |

---

## Descubrimiento dinamico de PKs y FKs

El AuthService NO hardcodea nombres de columnas. Los descubre consultando la API.

### Como funciona?

```
Llamada: GET /api/estructuras/rol_usuario/modelo

La API responde con las columnas y FKs:
{
  "datos": [
    {"column_name": "fkemail", "is_primary_key": "YES",
     "foreign_table_name": "usuario"},
    {"column_name": "fkidrol", "is_primary_key": "YES",
     "foreign_table_name": "rol"}
  ]
}

El AuthService extrae y cachea en _fk_cache:
  "rol_usuario->usuario" = "fkemail"     (FK hacia usuario)
  "rol_usuario->rol" = "fkidrol"         (FK hacia rol)
  "pk_usuario" = "email"                 (PK de usuario)
  "pk_rol" = "id"                        (PK de rol)
```

### Por que es importante?

Asi funciona con CUALQUIER base de datos sin importar como se llamen las columnas.
Si en otra BD el FK se llama `id_usuario` en vez de `fkemail`, el sistema lo descubre
automaticamente. No hay que cambiar codigo.

### Compatibilidad

- **PostgreSQL**: devuelve `foreign_table_name` directo en cada columna
- **SqlServer**: a veces no devuelve bien `foreign_table_name`, entonces
  busca como fallback en `fk_constraint_name` (ej: `fk_rolusuario_usuario`)

---

## Optimizaciones del login

| Optimizacion | Que hace | Por que |
|---|---|---|
| `_fk_cache` | Guarda PKs/FKs en memoria | No repite consultas a la API |
| `ConsultasController` | 1 consulta SQL con JOINs para roles + rutas | En vez de 5 GETs que traian tablas completas |
| `_rutas_cache` | obtener_roles_usuario cachea las rutas | obtener_rutas_permitidas no hace otra consulta |
| Cookie firmada | Persiste sesion al navegar y refrescar | No pide login en cada pagina |

### Comparacion: antes vs ahora

| Aspecto | Antes (5 GETs) | Ahora (1 SQL) |
|---------|---------------|---------------|
| Llamadas HTTP post-login | 5 | 1 |
| Datos transferidos | Tablas COMPLETAS | Solo filas del usuario |
| Donde se filtra | En memoria (Python) | En la BD (SQL WHERE) |
| Controlador usado | EntidadesController | ConsultasController |
| Endpoint | GET /api/{tabla}?limite=999999 | POST /api/consultas/ejecutarconsultaparametrizada |

---

## Las 5 tablas y su relacion (diagrama)

```
usuario --< rol_usuario >-- rol --< rutarol >-- ruta
(quien)    (tiene roles)  (que rol) (puede ver) (que pagina)

Ejemplo concreto:
  admin@correo.com tiene rol "Administrador" (id=1)
  Rol "Administrador" tiene acceso a /producto, /cliente, /factura
  -> admin@correo.com puede acceder a esas 3 paginas
  -> Si intenta /workflow -> "Acceso Denegado" (403)
  -> Si no hay rutas configuradas -> permite todo (sistema nuevo)
```

---

## ConsultasController: como se usa para cargar roles y rutas

### Que es ConsultasController?

Es un endpoint de la API generica C# que permite ejecutar consultas SQL
parametrizadas. A diferencia de EntidadesController (que hace CRUD tabla por tabla),
ConsultasController puede hacer JOINs de varias tablas en una sola llamada.

```
EntidadesController:  GET /api/usuario          -> trae TODA la tabla usuario
                      GET /api/rol              -> trae TODA la tabla rol
                      GET /api/rol_usuario      -> trae TODA la tabla rol_usuario
                      (3 llamadas, 3 tablas completas, filtrar en Python)

ConsultasController:  POST /api/consultas/ejecutarconsultaparametrizada
                      -> 1 consulta SQL con JOINs, WHERE filtra en la BD
                      -> solo viajan las filas de ESTE usuario
```

### Como se arma la consulta SQL

El auth_service arma la consulta DINAMICAMENTE usando los nombres de FK y PK
que descubrio de la estructura de la BD. Los nombres NO estan hardcodeados.

```
_obtener_pk/_obtener_fk descubren:
  pk_usuario = "email"
  pk_rol = "id"
  pk_ruta = "id"
  rol_usuario->usuario = "fkemail"
  rol_usuario->rol = "fkidrol"
  rutarol->rol = "fkidrol"
  rutarol->ruta = "fkidruta"

Con esos valores arma:

  SELECT r.nombre AS nombre_rol, ruta_t.ruta
  FROM usuario u
  JOIN rol_usuario rolu ON u.email = rolu.fkemail        <- descubierto
  JOIN rol r ON rolu.fkidrol = r.id                      <- descubierto
  JOIN rutarol rr ON r.id = rr.fkidrol                   <- descubierto
  JOIN ruta ruta_t ON rr.fkidruta = ruta_t.id            <- descubierto
  WHERE u.email = @email                                 <- parametrizado
```

### Que devuelve la consulta

Para un usuario con rol "Contador" y 3 rutas permitidas:

```json
{
  "resultados": [
    {"nombre_rol": "Contador", "ruta": "/home"},
    {"nombre_rol": "Contador", "ruta": "/cliente"},
    {"nombre_rol": "Contador", "ruta": "/producto"}
  ],
  "total": 3
}
```

### El parametro @email previene inyeccion SQL

La consulta usa `@email` como parametro, NO concatenacion de strings.
ConsultasController convierte `@email` a un parametro SQL seguro:

```
INSEGURO (concatenar):  WHERE u.email = '" + email + "'    <- inyeccion SQL posible
SEGURO (parametrizar):  WHERE u.email = @email              <- la BD escapa el valor
```

### Fallback: si ConsultasController no funciona

Si la API no tiene ConsultasController o si no se descubren los FK necesarios,
el auth_service usa automaticamente los metodos fallback (5 GETs separados).
Esto asegura que el login funcione aunque el endpoint de consultas no exista.

---

## Tabla resumen de endpoints usados en el login

| # | Momento | Endpoint | Controlador | Para que |
|---|---------|----------|-------------|----------|
| 1 | Login | `GET /api/estructuras/usuario/modelo` | EstructurasController | Descubrir PK de la tabla usuario |
| 2 | Login | `POST /api/autenticacion/token` | AutenticacionController | Verificar contrasena con BCrypt y generar JWT |
| 3 | Post-login | `POST /api/consultas/ejecutarconsultaparametrizada` | ConsultasController | Cargar roles y rutas con UNA sola consulta SQL |
| 4 | Cambiar clave | `PUT /api/usuario/{pk}/{val}?camposEncriptar=contrasena` | EntidadesController | Guardar nueva contrasena con BCrypt |

**Total: 3 llamadas HTTP para hacer login** (estructura + autenticacion + roles/rutas).

---

## Como funciona Cambiar Contrasena

### Cuando se activa?

Dos casos:
1. **Voluntario**: el usuario hace clic en "Cambiar contrasena"
2. **Forzado**: el sistema genera una contrasena temporal (recuperar) y obliga
   al usuario a cambiarla antes de poder usar la aplicacion

### Flujo completo

```
1. Usuario hace login con contrasena temporal
        |
        v
2. auth.py detecta: debe_cambiar_contrasena = True
   (porque el campo debe_cambiar_contrasena es True en la BD
    o porque el email esta marcado en _emails_debe_cambiar)
        |
        v
3. session["debe_cambiar_contrasena"] = True
   -> redirect a /cambiar-contrasena
        |
        v
4. Middleware TAMBIEN bloquea (doble proteccion):
   -> if session.get("debe_cambiar_contrasena") and path != "/cambiar-contrasena"
   -> Redirige a /cambiar-contrasena
   -> El usuario NO puede ir a ninguna otra pagina
        |
        v
5. cambiar_contrasena.html muestra formulario:
   -> Campo: nueva contrasena
   -> Campo: confirmar contrasena
        |
        v
6. Validacion en el backend (antes de enviar a la API):
   -> Las dos coinciden?         Si no -> "Las contrasenas no coinciden."
   -> Minimo 6 caracteres?       Si no -> "Minimo 6 caracteres."
   -> Tiene al menos 1 mayuscula? Si no -> "Debe incluir una mayuscula."
   -> Tiene al menos 1 numero?   Si no -> "Debe incluir un numero."
        |
        v
7. auth_service.actualizar_contrasena(email, nueva):
   -> PUT /api/usuario/{pk}/{email}?camposEncriptar=contrasena
   -> Body: {"contrasena": "NuevaContrasena123"}
        |
        v
8. La API C# recibe la peticion:
   -> Ve ?camposEncriptar=contrasena en la URL
   -> Ejecuta: BCrypt.HashPassword("NuevaContrasena123")
   -> Resultado: "$2a$12$xK9mN..."  (hash irreversible)
   -> Guarda el HASH en la BD (nunca el texto plano)
   -> La contrasena anterior desaparece para siempre
        |
        v
9. Si la API responde OK:
   -> session.pop("debe_cambiar_contrasena")
   -> Redirect a / (pagina de inicio)
   -> El usuario puede navegar normalmente
```

---

## Configurar Gmail para SMTP (recuperacion de contrasena)

La recuperacion de contrasena genera una temporal, la guarda con BCrypt,
y la envia por correo SMTP. Si SMTP no esta configurado, muestra la
temporal en pantalla (para desarrollo).

### Paso 1: Crear una cuenta de Gmail (si no tiene una para el proyecto)

1. Ir a https://accounts.google.com/signup
2. Crear una cuenta nueva (ej: `mi.proyecto.2026@gmail.com`)
3. Completar el registro con nombre, fecha de nacimiento, etc.
4. Agregar un numero de telefono (lo va a necesitar en el paso 2)

### Paso 2: Activar la verificacion en 2 pasos

Google NO permite crear App Passwords sin verificacion en 2 pasos.
Es un requisito obligatorio. Siga estos pasos:

1. Abrir el navegador e ir a: https://myaccount.google.com/security
2. Iniciar sesion con la cuenta de Gmail del paso 1
3. Bajar en la pagina hasta la seccion **"Como inicias sesion en Google"**
4. Buscar **"Verificacion en dos pasos"** (dira "desactivada")
5. Hacer clic en **"Verificacion en dos pasos"**
6. Se abre una pagina nueva. Hacer clic en el boton **"Activar verificacion en dos pasos"**
7. Google le pedira confirmar con su telefono:
   - Seleccionar el pais (+57 Colombia)
   - Escribir su numero de celular
   - Elegir "Mensaje de texto" o "Llamada"
   - Hacer clic en "Enviar"
8. Escribir el codigo de 6 digitos que le llego al celular
9. Hacer clic en **"Activar"**
10. Verificar que ahora dice **"Activada"** en la seccion de seguridad

### Paso 3: Crear una App Password (contrasena de aplicacion)

Una App Password es una contrasena especial de 16 caracteres que
solo sirve para aplicaciones externas. La contrasena normal de Gmail
NO funciona para SMTP.

1. Ir a: https://myaccount.google.com/apppasswords
   - Si no le deja entrar, es porque el paso 2 no se completo
   - Vuelva al paso 2 y verifique que la verificacion en 2 pasos esta "Activada"
2. En **"Nombre de la app"** escribir: `FlaskLogin` (o cualquier nombre)
3. Hacer clic en **"Crear"**
4. Google muestra una contrasena de 16 caracteres, algo como: `pcsa qfto hhjf sadv`
5. **Copiarla inmediatamente** — solo se muestra UNA vez
6. Si la pierde, puede crear otra (y la anterior deja de funcionar)

### Paso 4: Configurar config.py

Abrir `config.py` del proyecto y poner los datos:

```python
# SMTP (configurar para recuperacion de contrasena)
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "mi.proyecto.2026@gmail.com"        # La cuenta de Gmail del paso 1
SMTP_PASS = "pcsa qfto hhjf sadv"               # La App Password del paso 3 (NO la contrasena de Gmail)
SMTP_FROM = "mi.proyecto.2026@gmail.com"         # Misma cuenta (remitente)
```

### Paso 5: Probar

1. Ejecutar la aplicacion Flask
2. Ir a `/recuperar-contrasena`
3. Escribir un email que exista en la tabla `usuario`
4. Si todo esta bien, llega un correo con la contrasena temporal
5. Si SMTP no esta configurado, muestra la temporal en pantalla

### Si algo no funciona

| Problema | Solucion |
|----------|----------|
| "App passwords not available" | El paso 2 no se completo. Verificar que dice "Activada" |
| "Username and Password not accepted" | Usar la App Password del paso 3, NO la contrasena de Gmail |
| "SMTP no configurado" | Llenar SMTP_USER y SMTP_PASS en config.py |
| "Connection refused" | Verificar que el firewall no bloquee el puerto 587 |
| No llega el correo | Revisar la carpeta de **spam** del destinatario |
| Perdio la App Password | Ir al paso 3 y crear una nueva |

### Alternativas a Gmail

| Proveedor | Host | Puerto | Notas |
|-----------|------|--------|-------|
| Gmail | smtp.gmail.com | 587 | Requiere App Password (pasos 2 y 3) |
| Outlook/Hotmail | smtp-mail.outlook.com | 587 | Contrasena normal funciona |
| Yahoo | smtp.mail.yahoo.com | 587 | Requiere App Password |
| Mailtrap (pruebas) | sandbox.smtp.mailtrap.io | 587 | Gratis para desarrollo, no envia correos reales |

---

## Forma anterior sin ConsultasController (referencia)

Antes de usar ConsultasController, el login usaba 5+ llamadas HTTP al CRUD generico.
Esta forma todavia funciona como fallback si ConsultasController no esta disponible.

### Endpoints que usaba (forma anterior)

| # | Momento | Endpoint | Para que |
|---|---------|----------|----------|
| 1 | Login | `GET /api/estructuras/usuario/modelo` | Descubrir PK |
| 2 | Login | `POST /api/autenticacion/token` | Verificar BCrypt, generar JWT |
| 3 | Post-login | `GET /api/usuario?limite=999999` | Traer TODOS los usuarios, buscar nombre |
| 4 | Post-login | `GET /api/rol_usuario?limite=999999` | Traer TODOS los rol_usuario, filtrar por email |
| 5 | Post-login | `GET /api/rol?limite=999999` | Traer TODOS los roles, mapear id a nombre |
| 6 | Post-login | `GET /api/rutarol?limite=999999` | Traer TODOS los rutarol, filtrar por rol |
| 7 | Post-login | `GET /api/ruta?limite=999999` | Traer TODAS las rutas, mapear id a path |

**Total: 7 llamadas HTTP** (2 + 5 GETs al CRUD generico).

### Problema de esta forma

Cada GET traia la tabla **COMPLETA** con `?limite=999999`. Si habia:
- 500 usuarios -> traia 500 para buscar 1
- 200 roles_usuario -> traia 200 para filtrar los de 1 email
- 50 rutarol -> traia 50 para filtrar 5

Toda la logica de filtrado se hacia en memoria (Python), no en la BD.

### Por que se cambio

```
ANTES: 5 GETs x tabla completa x filtrar en Python
  -> 5 llamadas HTTP
  -> Miles de registros transferidos
  -> CPU del frontend filtrando

AHORA: 1 POST con SQL x filtrar en BD
  -> 1 llamada HTTP
  -> Solo las filas del usuario
  -> CPU de la BD filtrando (mas eficiente)
```

### Codigo fallback

Los metodos `_obtener_roles_fallback()` y `_obtener_rutas_fallback()` en
auth_service.py conservan la logica anterior para usarla si ConsultasController
no esta disponible. Se activan automaticamente si no se descubren los
FKs necesarios para armar la consulta SQL.

---

## Probar el login

### 1. Preparar

1. Asegurese de que la API C# este corriendo (puerto 5035)
2. Cree un usuario con contrasena encriptada:
   ```
   POST http://localhost:5035/api/usuario?camposEncriptar=contrasena
   Body: {"email": "admin@test.com", "contrasena": "Admin123"}
   ```
3. Cree un rol y asignelo:
   ```
   POST http://localhost:5035/api/rol
   Body: {"nombre": "Administrador"}

   POST http://localhost:5035/api/rol_usuario
   Body: {"fkemail": "admin@test.com", "fkidrol": 1}
   ```

### 2. Probar login

4. Ejecute: `python app.py`
5. Abra el navegador -> redirige a `/login`
6. Ingrese credenciales -> deberia entrar
7. Verifique en F12 -> Application -> Cookies:
   - session (cookie firmada con todos los datos)

### 3. Probar control de acceso

8. Asigne rutas al rol (en la tabla `rutarol`):
   ```
   POST http://localhost:5035/api/ruta
   Body: {"ruta": "/producto", "descripcion": "Gestion de productos"}

   POST http://localhost:5035/api/rutarol
   Body: {"fkidrol": 1, "fkidruta": 1}
   ```
9. Cierre sesion y vuelva a entrar (para que cargue las rutas nuevas)
10. Navegue a `/producto` -> deberia funcionar (tiene permiso)
11. Navegue a `/workflow` -> deberia mostrar "Acceso Denegado" (403)
12. Escriba `/workflow` en la barra de direcciones -> mismo resultado (middleware lo detecta)

### 4. Probar JWT (opcional)

13. En la API C#, agregue `[Authorize]` a un controller
14. Sin hacer login, intente desde Postman: `GET /api/usuario` -> 401 Unauthorized
15. Haga login en Flask, copie el token de la cookie de sesion
16. En Postman, agregue header: `Authorization: Bearer {token}` -> 200 OK

### 5. Probar cambiar contrasena

17. Vaya a `/recuperar-contrasena`
18. Ingrese el email del usuario
19. Si SMTP esta configurado -> llega correo con temporal
20. Si SMTP no esta configurado -> muestra la temporal en pantalla
21. Haga login con la temporal -> redirige a `/cambiar-contrasena` (forzado)
22. Escriba nueva contrasena (minimo 6 chars, 1 mayuscula, 1 numero)
23. Confirme -> redirige a `/` y puede navegar normalmente
