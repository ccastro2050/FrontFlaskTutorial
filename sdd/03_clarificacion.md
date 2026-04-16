# Etapa 3: Clarificacion

> Segun [Spec-Kit de GitHub](https://github.com/github/spec-kit): la clarificacion
> (`/speckit.clarify`) resuelve ambiguedades ANTES de la planificacion tecnica,
> reduciendo retrabajos posteriores. "La IA te hace preguntas sobre lo que olvidaste.
> Te fuerza a pensar para no dejar agujeros."
>
> Referencia: [spec-driven.md](https://github.com/github/spec-kit/blob/main/spec-driven.md)

---

## 1. Preguntas resueltas sobre la arquitectura

### P: Por que Flask y no Django?
**R:** Flask es un microframework sin magia. El estudiante ve cada linea de codigo y entiende que hace. Django tiene ORM, admin, auth integrado — el estudiante no aprende como funciona por debajo. Flask obliga a construir todo manualmente, que es el objetivo del tutorial.

### P: Por que no usar SQLAlchemy si Flask lo soporta?
**R:** Porque el frontend no accede a la BD. Todo va por HTTP a la API REST. Si usamos SQLAlchemy, el estudiante aprende ORM pero no aprende a consumir APIs, que es lo que necesita en el mundo real (microservicios, frontends desacoplados).

### P: Por que la API es en C# y no en Python?
**R:** Para que el estudiante entienda que frontend y backend son independientes. Si ambos fueran Python, podria confundir Flask con la API. Con C# queda claro: Flask es el frontend, C# es el backend, se comunican por HTTP.

### P: Que pasa si la API no esta corriendo?
**R:** Los servicios (`ApiService`, `AuthService`) tienen `try/except` que capturan `requests.RequestException`. Si la API no responde, se muestra un mensaje de error en pantalla sin que la app crashee. El login falla con "Error de conexion".

## 2. Preguntas resueltas sobre seguridad

### P: Si la sesion es una cookie, el usuario puede manipularla?
**R:** Flask firma la cookie con `SECRET_KEY` usando HMAC. Si el usuario cambia un byte, la firma no coincide y Flask la invalida. No puede inyectar roles ni rutas.

### P: Por que guardar el JWT si Flask ya tiene sesion?
**R:** Son dos capas diferentes:
- La **sesion Flask** protege las paginas del frontend (middleware verifica antes de cada request)
- El **JWT** protege los datos de la API (si tiene `[Authorize]`, rechaza sin token)

Sin JWT, alguien puede abrir Postman y hacer `DELETE /api/usuario/email/admin@test.com` sin haber hecho login.

### P: Que pasa si el JWT expira durante la sesion?
**R:** La API responde 401. El ApiService no maneja esto automaticamente — el usuario ve un error y debe hacer login de nuevo. En un sistema de produccion se implementaria refresh token, pero esta fuera del alcance del tutorial.

### P: Por que no usar Spring Security / Passport.js / otro framework de auth?
**R:** Porque el objetivo es que el estudiante **entienda** como funciona la autenticacion. Si usa un framework de auth, solo configura y no aprende. Construirlo manualmente ensena: BCrypt, JWT, sesion, middleware, roles, rutas.

### P: Las contrasenas viajan en texto plano por HTTP?
**R:** Si, en desarrollo local (http://localhost). En produccion se usa HTTPS. La contrasena viaja en el body del POST (no en la URL) y solo el servidor la lee. La API inmediatamente la compara con el hash BCrypt — nunca la guarda en texto plano.

## 3. Preguntas resueltas sobre el CRUD

### P: Como sabe el formulario que tipo de input usar para cada campo?
**R:** Los templates tienen los tipos hardcodeados por tabla (ej: `type="email"` para email, `type="number"` para precio). En el generador generico (`frontGenericoFlask`), se descubre el tipo via `/api/estructuras/basedatos` y se mapea: `varchar -> text`, `integer -> number`, `boolean -> checkbox`, etc.

### P: Que pasa con los campos FK en los formularios?
**R:** Se renderizan como `<select>` cargados desde la API. Ejemplo: en factura, el campo `fkcodvendedor` se muestra como un dropdown con todos los vendedores. El template hace `{% for v in vendedores %}` para llenar las opciones.

### P: Y si una tabla tiene muchos registros (1000+)?
**R:** Se usa `?limite=N` en la URL de la API. Los CRUDs del tutorial no implementan paginacion — traen todo con `?limite=999999`. En produccion se implementaria paginacion real (fuera del alcance).

### P: Como se manejan los errores de la API (400, 404, 500)?
**R:** `ApiService` retorna tupla `(exito, mensaje)`. La ruta usa `flash(mensaje, "danger")` para mostrar el error al usuario. No se propagan excepciones al template.

## 4. Preguntas resueltas sobre el descubrimiento dinamico

### P: Por que no hardcodear "fkemail" y "fkidrol"?
**R:** Porque si otra BD usa `id_usuario` o `email_usuario`, el codigo deja de funcionar. El descubrimiento dinamico via `/api/estructuras/basedatos` permite que el mismo codigo funcione con cualquier BD que tenga las 5 tablas de auth, sin importar como se llamen las columnas.

### P: Que pasa si la API no tiene el endpoint /api/estructuras?
**R:** El `AuthService` tiene metodos fallback (`_obtener_roles_fallback`, `_obtener_rutas_fallback`) que usan GETs separados al CRUD generico. Si los FKs no se descubren, se activa el fallback automaticamente.

### P: Por que usar ConsultasController en vez de los 5 GETs?
**R:** Eficiencia. Los 5 GETs traen tablas COMPLETAS y filtran en Python. ConsultasController ejecuta 1 SQL con JOINs y WHERE en la BD — solo viajan las filas del usuario. Referencia: Paso12_LoginYControlDeAcceso.md, seccion "ConsultasController".

## 5. Preguntas resueltas sobre el trabajo colaborativo

### P: Que pasa si dos estudiantes crean la misma ruta?
**R:** Conflicto de merge en `app.py`. Se resuelve en la rama feature/ antes de mergear a main. Por eso cada estudiante tiene tablas asignadas (Paso0).

### P: Que pasa si un estudiante instala un paquete nuevo?
**R:** Debe hacer `pip freeze > requirements.txt` y commitear el cambio. Si no lo hace, el proyecto del otro estudiante falla con `ModuleNotFoundError`.

### P: Quien resuelve conflictos de merge?
**R:** El Estudiante 1 (admin/scrum master). Los otros hacen `git fetch origin` y mergean main a su rama antes de hacer PR.

## 6. Decisiones de diseno documentadas

| Decision | Alternativa descartada | Razon |
|----------|----------------------|-------|
| Flask (microframework) | Django (fullstack) | El estudiante ve todo, nada es magia |
| Jinja2 (templates server-side) | React/Vue (SPA) | Menos complejidad, un solo lenguaje |
| requests (HTTP client) | httpx, aiohttp | Sincrono y simple, sin async |
| session (cookie firmada) | JWT-only (stateless) | Flask lo trae integrado, facil de ensenar |
| ConsultasController (1 SQL) | 5 GETs separados | Eficiencia, menos trafico de red |
| Bootstrap CDN | Tailwind, Material UI | Sin build tools, funciona con un link |
| Descubrimiento dinamico FK/PK | Hardcodear nombres | Funciona con cualquier BD |
| Middleware before_request | Decorador @login_required | Protege TODAS las rutas automaticamente |
| PostgreSQL | MySQL, SQLite | ACID completo, soporte de JSON, compatible con SqlServer |
| 3FN (normalizacion) | Desnormalizar para rendimiento | Integridad sobre velocidad en sistema transaccional |
| Tablas intermedias N:M | Arrays en columna | 1FN: valores atomicos, sin grupos repetidos |

## 7. Preguntas resueltas sobre el modelo de datos

### P: Por que cliente tiene FK a persona Y a empresa?
**R:** Un cliente puede ser persona natural (fkcodpersona) O persona juridica (fkcodempresa). `fkcodempresa` es nullable — si es persona natural, no tiene empresa. Esto cumple 3FN porque el nombre de la persona no se duplica en la tabla cliente.

### P: Por que productosporfactura tiene su propio campo "precio"?
**R:** Porque el precio del producto puede cambiar en el futuro. Si solo guardamos el FK al producto, al consultar una factura vieja mostraria el precio actual, no el que se cobro. Guardar el precio al momento de la venta es un patron estandar de facturacion.

### P: Por que usuario tiene email como PK y no un id numerico?
**R:** Porque el email es unico y natural — es lo que el usuario escribe para hacer login. Usar un id numerico obligaria a hacer un JOIN extra para buscar por email. Ademas, simplifica las FKs en rol_usuario (`fkemail` es legible).

### P: Por que las tablas de seguridad (rol, ruta, rutarol) estan separadas de las de negocio?
**R:** Principio de Single Responsibility (SOLID - S). Las tablas de negocio (producto, factura) manejan datos del dominio. Las tablas de seguridad (rol, ruta) manejan permisos. Si un dia se cambia el sistema de permisos, no se tocan las tablas de negocio.

### P: Por que no usar herencia de tablas (una tabla padre "persona" para cliente y vendedor)?
**R:** Porque PostgreSQL no soporta herencia de tablas de forma estandar (SQL Server tampoco). Ademas, cliente y vendedor tienen atributos diferentes (credito vs comision). Usar tablas separadas es mas simple y portable.

### P: Por que ACID y no BASE (eventual consistency)?
**R:** Este es un sistema transaccional (facturas, contrasenas, permisos). ACID garantiza que una factura se crea completa o no se crea. BASE es para sistemas distribuidos de alta escala (redes sociales, IoT) donde se acepta inconsistencia temporal. Un sistema de facturacion NO puede tener inconsistencia temporal — el dinero no puede "eventualmente" cuadrar.

## 8. Principios de diseno aplicados (resumen)

| Principio | Categoria | Donde aplica | Referencia |
|-----------|-----------|-------------|------------|
| SOLID - S (Single Responsibility) | OOP | Cada archivo/clase tiene 1 responsabilidad | 01_constitucion.md, Art. VII |
| SOLID - O (Open/Closed) | OOP | Agregar CRUD = archivos nuevos, no modificar existentes | 01_constitucion.md, Art. VII |
| SOLID - D (Dependency Inversion) | OOP | Routes dependen de ApiService, no de requests | 01_constitucion.md, Art. VII |
| ACID | BD | PostgreSQL garantiza transacciones integras | 01_constitucion.md, Art. VIII |
| 3FN (Normalizacion) | BD | Sin datos redundantes, FKs para relaciones | 02_especificacion.md, seccion ER |
| MVC | Arquitectura | services/ + templates/ + routes/ | 01_constitucion.md, Art. II |
| Facade | Patron | ApiService oculta complejidad HTTP | 01_constitucion.md, Art. IX |
| Strategy (fallback) | Patron | ConsultasController o 5 GETs segun disponibilidad | 01_constitucion.md, Art. IX |
| Middleware/Interceptor | Patron | before_request verifica auth en CADA request | 01_constitucion.md, Art. IX |
