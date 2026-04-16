# Etapa 4: Plan de Implementacion

> Segun [Spec-Kit](https://github.com/github/spec-kit): el plan traduce los requisitos de la
> especificacion en decisiones tecnicas concretas. "Cada eleccion de tecnologia tiene una
> rationale documentada." El plan se genera con `/speckit.plan` y el humano lo valida.
>
> Referencia: [plan-template.md](https://github.com/github/spec-kit/blob/main/templates/plan-template.md)

---

## 1. Resumen tecnico

Frontend web en Flask que consume la API generica C# via HTTP.
Arquitectura MVC adaptada: routes (controladores) + services (logica) + templates (vistas).
Autenticacion con BCrypt + JWT + sesion Flask.
Control de acceso por roles y rutas con middleware `before_request`.

## 2. Estructura de archivos del proyecto

```
FrontFlaskTutorial/
├── app.py                           <- Punto de entrada: crea Flask, registra todo
├── config.py                        <- API_BASE_URL, SECRET_KEY, SMTP
├── requirements.txt                 <- flask, requests
├── .gitignore                       <- venv/, __pycache__/, *.pyc
│
├── services/
│   ├── __init__.py
│   ├── api_service.py               <- CRUD generico: listar, crear, actualizar, eliminar
│   ├── auth_service.py              <- Login, roles, rutas, ConsultasController, fallback
│   └── email_service.py             <- SMTP para contrasena temporal
│
├── routes/
│   ├── __init__.py
│   ├── home.py                      <- /
│   ├── auth.py                      <- /login, /logout, /cambiar-contrasena, /recuperar
│   ├── producto.py                  <- /producto (CRUD)
│   ├── persona.py                   <- /persona (CRUD)
│   ├── usuario.py                   <- /usuario (CRUD)
│   ├── cliente.py                   <- /cliente (CRUD con FK persona, empresa)
│   ├── empresa.py                   <- /empresa (CRUD)
│   ├── vendedor.py                  <- /vendedor (CRUD)
│   ├── rol.py                       <- /rol (CRUD)
│   ├── ruta.py                      <- /ruta (CRUD)
│   └── factura.py                   <- /factura (maestro-detalle)
│
├── middleware/
│   └── auth_middleware.py           <- before_request + context_processor
│
├── templates/
│   ├── layout/
│   │   └── base.html                <- Layout: sidebar + top-row + content + Bootstrap
│   ├── components/
│   │   └── nav_menu.html            <- Menu lateral colapsable
│   └── pages/
│       ├── home.html                <- Pagina inicio
│       ├── login.html               <- Formulario login
│       ├── cambiar_contrasena.html   <- Cambiar contrasena
│       ├── recuperar_contrasena.html <- Recuperar contrasena
│       ├── sin_acceso.html           <- Error 403
│       ├── producto.html             <- CRUD producto
│       ├── persona.html              <- CRUD persona
│       ├── usuario.html              <- CRUD usuario
│       ├── cliente.html              <- CRUD con selects FK
│       ├── empresa.html              <- CRUD empresa
│       ├── vendedor.html             <- CRUD vendedor
│       ├── rol.html                  <- CRUD rol
│       ├── ruta.html                 <- CRUD ruta
│       └── factura.html              <- Maestro-detalle
│
├── static/css/
│   └── app.css                      <- Variables CSS, estilos custom
│
├── scripts_bds/                     <- SQL para crear tablas
│
└── sdd/                             <- Documentacion SDD (estos archivos)
```

## 3. Orden de implementacion (por pasos)

> Cada paso corresponde a un Paso{N}.md del tutorial y a una o mas ramas feature/.

| Orden | Paso | Que se implementa | Dependencias | Estudiante |
|-------|------|--------------------|-------------|------------|
| 1 | Paso 0 | Plan de desarrollo, reglas | Ninguna | Todos |
| 2 | Paso 3 | Proyecto base: app.py, config.py, git | Paso 0 | Est. 1 |
| 3 | Paso 4 | ApiService (CRUD generico HTTP) | Paso 3 | Est. 1 |
| 4 | Paso 5 | Layout base, nav_menu, home | Paso 4 | Est. 1 |
| 5 | Paso 6 | CRUD producto | Paso 5 | Est. 1 |
| 6 | Paso 7 | CRUD persona + usuario | Paso 5 | Est. 2 + 3 |
| 7 | Paso 8 | CRUD empresa, cliente, rol | Paso 7 | Est. 2 |
| 8 | Paso 9 | CRUD ruta, vendedor, nav_menu | Paso 7 | Est. 3 |
| 9 | Paso 10 | Factura maestro-detalle | Paso 8+9 | Est. 2 |
| 10 | Paso 12 | Login + JWT + middleware + roles | Paso 9 | Est. 1 |

### Diagrama de dependencias

```
Paso 0 (plan)
  |
  v
Paso 3 (proyecto base)
  |
  v
Paso 4 (ApiService)
  |
  v
Paso 5 (layout + nav + home)
  |
  +-------+-------+
  v       v       v
Paso 6  Paso 7  (paralelo: producto, persona+usuario)
  |       |
  v       +-------+
  |       v       v
  |     Paso 8  Paso 9  (paralelo: empresa+cliente, ruta+vendedor)
  |       |       |
  |       v       v
  |     Paso 10   |   (factura, depende de 8+9)
  |               |
  +-------+-------+
          v
        Paso 12 (login + seguridad)
```

## 4. Modelo de datos

### Tablas CRUD (negocio)

| Tabla | PK | Campos clave | FKs |
|-------|-----|-------------|-----|
| producto | codigo | nombre, precio, existencia | - |
| persona | codigo | nombre, telefono, direccion | - |
| empresa | codigo | nombre, nit, direccion | - |
| cliente | id | credito | fkcodpersona->persona, fkcodempresa->empresa |
| vendedor | codigo | nombre, comision | - |
| usuario | email | contrasena (BCrypt), nombre | - |
| factura | numfactura | fecha, total | fkcodvendedor->vendedor, fkcodcliente->cliente |
| productosporfactura | id | cantidad, precio | fknumfact->factura, fkcodprod->producto |

### Tablas de seguridad (auth)

| Tabla | PK | Campos | FKs |
|-------|-----|--------|-----|
| rol | id | nombre | - |
| rol_usuario | id | - | fkemail->usuario, fkidrol->rol |
| ruta | id | ruta, descripcion | - |
| rutarol | id | - | fkidrol->rol, fkidruta->ruta |

## 5. Decisiones tecnicas

| Decision | Alternativa | Razon |
|----------|-------------|-------|
| ConsultasController (1 SQL) | 5 GETs separados | Eficiencia: BD filtra, no Python |
| Cookie firmada (Flask session) | JWT stateless | Flask lo trae integrado |
| `requests` sincrono | `httpx` async | Simplicidad para tutorial |
| Bootstrap CDN | npm install | Sin build tools |
| Middleware before_request | Decorador @login_required | Protege TODO automaticamente |
| context_processor | Pasar vars manual | Inyecta en todas las templates |

## 6. Endpoints de la API utilizados

### CRUD generico (cada tabla)

```
GET    /api/{tabla}?limite=N           <- Listar
POST   /api/{tabla}                    <- Crear
PUT    /api/{tabla}/{pk}/{valor}       <- Actualizar
DELETE /api/{tabla}/{pk}/{valor}       <- Eliminar
```

### Autenticacion y seguridad

```
POST   /api/autenticacion/token        <- Login BCrypt + JWT
GET    /api/estructuras/basedatos      <- Descubrir PKs/FKs
POST   /api/consultas/ejecutar...      <- SQL JOINs roles/rutas
PUT    /api/usuario/{pk}/{val}?camposEncriptar=contrasena  <- Cambiar clave
```

---

## 7. Diagramas de secuencia

> Los diagramas de secuencia muestran la interaccion entre componentes en el tiempo.
> Formato: [Mermaid](https://mermaid.js.org/) — se renderiza automaticamente en GitHub.

### 7.1 Secuencia: Login completo

```mermaid
sequenceDiagram
    actor U as Usuario
    participant N as Navegador
    participant M as Middleware<br>(auth_middleware.py)
    participant R as AuthController<br>(routes/auth.py)
    participant A as AuthService<br>(services/auth_service.py)
    participant API as API Generica C#<br>(puerto 5035)
    participant BD as PostgreSQL

    U->>N: Abre http://localhost:5300
    N->>M: GET /
    M->>M: session("usuario") existe?
    M-->>N: No -> redirect /login
    N->>U: Muestra formulario login

    U->>N: Escribe email + contrasena
    N->>R: POST /login (email, contrasena)
    R->>A: auth.login(email, contrasena)

    Note over A,API: PASO 1: Descubrir estructura BD
    A->>API: GET /api/estructuras/basedatos
    API->>BD: Consulta information_schema
    BD-->>API: Tablas, columnas, PKs, FKs
    API-->>A: JSON con estructura completa
    A->>A: Cachear PKs y FKs en _fk_cache

    Note over A,API: PASO 2: Autenticar con BCrypt
    A->>API: POST /api/autenticacion/token<br>{tabla, campoUsuario, campoContrasena, usuario, contrasena}
    API->>BD: SELECT contrasena FROM usuario WHERE email = ?
    BD-->>API: Hash BCrypt
    API->>API: BCrypt.Verify(contrasena, hash)
    alt Contrasena correcta
        API-->>A: 200 OK + JWT token
    else Contrasena incorrecta
        API-->>A: 401 Unauthorized
        A-->>R: (false, "Credenciales incorrectas")
        R-->>N: redirect /login + flash "danger"
        N-->>U: Muestra error
    end

    Note over A,API: PASO 3: Cargar roles y rutas (1 SQL)
    A->>A: Armar SQL dinamico con FKs descubiertos
    A->>API: POST /api/consultas/ejecutarconsultaparametrizada<br>{consulta: "SELECT r.nombre, ruta_t.ruta FROM usuario u JOIN...", parametros: {email}}
    API->>BD: Ejecuta SQL con JOINs de 5 tablas
    BD-->>API: Filas: [{nombre_rol, ruta}, ...]
    API-->>A: JSON con resultados
    A->>A: Extraer roles unicos + rutas unicas

    Note over R: Guardar en sesion Flask
    R->>R: session["token"] = JWT
    R->>R: session["usuario"] = email
    R->>R: session["roles"] = [roles]
    R->>R: session["rutas_permitidas"] = [rutas]
    R-->>N: redirect / + flash "Bienvenido"
    N->>M: GET /
    M->>M: session("usuario") existe? Si
    M->>M: ruta "/" siempre accesible
    M-->>N: Permite -> renderiza home.html
    N-->>U: Muestra pagina inicio con sidebar
```

### 7.2 Secuencia: CRUD Listar con JWT

```mermaid
sequenceDiagram
    actor U as Usuario
    participant N as Navegador
    participant M as Middleware
    participant R as Blueprint<br>(routes/producto.py)
    participant S as ApiService<br>(services/api_service.py)
    participant API as API Generica C#
    participant BD as PostgreSQL

    U->>N: Clic en "Productos" del menu
    N->>M: GET /producto
    M->>M: session("usuario") existe? Si
    M->>M: "/producto" en rutas_permitidas? Si
    M-->>R: Permite -> ejecuta index()

    R->>S: api.listar("producto")
    S->>S: _headers() -> lee session["token"]
    S->>API: GET /api/producto?limite=999999<br>Header: Authorization: Bearer eyJhbG...
    API->>API: Verificar JWT (firma + expiracion)
    alt JWT valido
        API->>BD: SELECT * FROM producto
        BD-->>API: Registros
        API-->>S: 200 OK + {datos: [...]}
    else JWT invalido o expirado
        API-->>S: 401 Unauthorized
        S-->>R: Lista vacia
    end
    S-->>R: Lista de diccionarios
    R->>N: render_template("pages/producto.html", datos=datos)
    N-->>U: Muestra tabla HTML con productos
```

### 7.3 Secuencia: CRUD Crear

```mermaid
sequenceDiagram
    actor U as Usuario
    participant N as Navegador
    participant M as Middleware
    participant R as Blueprint<br>(routes/producto.py)
    participant S as ApiService
    participant API as API Generica C#
    participant BD as PostgreSQL

    U->>N: Llena formulario + clic "Guardar"
    N->>R: POST /producto/crear<br>Form: {codigo, nombre, precio}
    R->>R: datos = dict(request.form)
    R->>S: api.crear("producto", datos)
    S->>API: POST /api/producto<br>Header: Authorization: Bearer ...<br>Body: {codigo, nombre, precio}
    API->>BD: INSERT INTO producto VALUES (...)
    BD-->>API: OK
    API-->>S: 200 + {mensaje: "Registro creado"}
    S-->>R: (True, "Registro creado")
    R->>R: flash("Registro creado", "success")
    R-->>N: redirect /producto
    N->>M: GET /producto (repite flujo listar)
    N-->>U: Muestra tabla actualizada + alerta verde
```

### 7.4 Secuencia: Acceso denegado

```mermaid
sequenceDiagram
    actor U as Usuario
    participant N as Navegador
    participant M as Middleware

    U->>N: Escribe /factura en la barra de direcciones
    N->>M: GET /factura
    M->>M: session("usuario") existe? Si
    M->>M: "/factura" en rutas_permitidas?
    M->>M: No esta en la lista
    M-->>N: render_template("sin_acceso.html"), 403
    N-->>U: Muestra "Acceso Denegado" con boton "Volver"
```

### 7.5 Secuencia: Cambiar contrasena

```mermaid
sequenceDiagram
    actor U as Usuario
    participant N as Navegador
    participant R as AuthController
    participant A as AuthService
    participant API as API Generica C#
    participant BD as PostgreSQL

    U->>N: Navega a /cambiar-contrasena
    N-->>U: Muestra formulario (nueva + confirmar)
    U->>N: Escribe nueva contrasena + confirmar
    N->>R: POST /cambiar-contrasena (nueva, confirmar)
    R->>R: Validar: coinciden? 6+ chars? mayuscula? numero?
    alt Validacion falla
        R-->>N: redirect + flash "danger"
        N-->>U: Muestra error
    end
    R->>A: auth.actualizar_contrasena(email, nueva)
    A->>A: pk = obtenerPK("usuario") -> "email"
    A->>API: PUT /api/usuario/email/{email}?camposEncriptar=contrasena<br>Body: {contrasena: "NuevaClave123"}
    API->>API: BCrypt.HashPassword("NuevaClave123") -> "$2a$12$..."
    API->>BD: UPDATE usuario SET contrasena = "$2a$12$..." WHERE email = ?
    BD-->>API: OK
    API-->>A: 200 OK
    A-->>R: (True, "Contrasena actualizada")
    R-->>N: redirect / + flash "success"
    N-->>U: Pagina inicio con alerta "Contrasena actualizada"
```

---

## 8. Diagrama de clases

> Muestra las clases Python del proyecto, sus atributos, metodos y relaciones.
> Formato: [Mermaid](https://mermaid.js.org/) — se renderiza en GitHub.

### 8.1 Diagrama de clases completo

```mermaid
classDiagram
    direction TB

    class Flask {
        +secret_key: str
        +register_blueprint(bp)
        +run(port)
    }

    class ApiService {
        -base_url: str
        +_headers() dict
        +listar(tabla, limite) list
        +crear(tabla, datos) tuple
        +actualizar(tabla, pk, valor, datos) tuple
        +eliminar(tabla, pk, valor) tuple
        +ejecutar_sp(nombre_sp, parametros) tuple
    }

    class AuthService {
        -base_url: str
        -session: requests.Session
        -_fk_cache: dict
        -_rutas_cache: set
        +login(email, contrasena) tuple
        +obtener_roles_y_rutas(email) tuple
        +obtener_roles_usuario(email) list
        +obtener_rutas_permitidas(roles) set
        +obtener_datos_usuario(email) dict
        +actualizar_contrasena(email, nueva) tuple
        -_post_consulta(sql, parametros) list
        -_obtener_estructura(tabla) list
        -_obtener_fk(origen, destino) str
        -_obtener_pk(tabla) str
        -_obtener_roles_fallback(email) list
        -_obtener_rutas_fallback(roles) set
    }

    class EmailService {
        +enviar_correo(destinatario, asunto, body) bool
        +enviar_contrasena_temporal(destinatario, pwd) bool
    }

    class AuthMiddleware {
        -RUTAS_PUBLICAS: list
        +crear_middleware(app)
        +verificar_autenticacion()
        +inyectar_sesion() dict
    }

    class BlueprintHome {
        +index() Response
    }

    class BlueprintProducto {
        +index() Response
        +crear() Response
        +editar(id) Response
        +eliminar(id) Response
    }

    class BlueprintAuth {
        +login() Response
        +login_post() Response
        +logout() Response
        +cambiar_contrasena() Response
        +cambiar_contrasena_post() Response
        +recuperar_contrasena() Response
        +recuperar_contrasena_post() Response
    }

    class BlueprintFactura {
        +index() Response
        +crear() Response
        +ver(id) Response
        +eliminar(id) Response
    }

    Flask --> AuthMiddleware : registra before_request
    Flask --> BlueprintHome : register_blueprint
    Flask --> BlueprintProducto : register_blueprint
    Flask --> BlueprintAuth : register_blueprint
    Flask --> BlueprintFactura : register_blueprint

    BlueprintProducto --> ApiService : usa para CRUD
    BlueprintFactura --> ApiService : usa para CRUD
    BlueprintHome --> ApiService : usa para datos

    BlueprintAuth --> AuthService : usa para login/roles
    BlueprintAuth --> EmailService : usa para recuperar pwd

    AuthMiddleware --> Flask : inyecta context_processor

    ApiService ..> Flask : lee session["token"] via _headers()
    AuthService ..> ApiService : NO depende (usa requests directo)

    note for AuthService "Descubrimiento dinamico FK/PK\nConsultasController (1 SQL)\nFallback: 5 GETs separados"
    note for ApiService "JWT en header Authorization\nFacade sobre la API REST"
    note for AuthMiddleware "before_request en CADA request\nVerifica sesion + rutas_permitidas"
```

### 8.2 Relaciones entre clases

| Relacion | Tipo | Descripcion |
|----------|------|-------------|
| Flask -> AuthMiddleware | Composicion | Flask registra el middleware al iniciar |
| Flask -> Blueprints | Composicion | Flask registra todos los blueprints |
| Blueprints -> ApiService | Dependencia | Los blueprints CRUD usan ApiService para HTTP |
| BlueprintAuth -> AuthService | Dependencia | Auth usa AuthService para login/roles |
| BlueprintAuth -> EmailService | Dependencia | Auth usa EmailService para recuperar pwd |
| ApiService ..> Flask session | Uso | Lee token JWT de la sesion para _headers() |
| AuthService --|> ApiService | Independiente | AuthService NO depende de ApiService (usa requests directo) |

### 8.3 Por que AuthService es independiente de ApiService?

```
AuthService usa requests.Session() directo, NO ApiService.

Razon: ApiService puede tener firmas diferentes segun el proyecto
(listar vs listarAsync, parametros distintos, etc).
AuthService con requests directo funciona en CUALQUIER proyecto Flask.

AuthService                    ApiService
  |                              |
  +-- requests.Session()         +-- requests.get/post/put/delete
  |   (HTTP directo)             |   (con _headers() JWT)
  v                              v
  API Generica C#                API Generica C#
```

---

## Referencias Spec-Kit

- Formato plan: [plan-template.md](https://github.com/github/spec-kit/blob/main/templates/plan-template.md)
- Principio de simplicidad: [spec-driven.md, Articulo VII](https://github.com/github/spec-kit/blob/main/spec-driven.md)
- Flujo SDD: [README de Spec-Kit](https://github.com/github/spec-kit)
- Mermaid (diagramas): [mermaid.js.org](https://mermaid.js.org/)
