# Paso 12: Login y Control de Acceso

## Los 3 conceptos clave de seguridad

1. **Autenticacion** → ¿Quien eres? (login, BCrypt, JWT)
2. **Autorizacion** → ¿Que puedes hacer? (roles, rutas, permisos)
3. **Encriptacion** → ¿Como se protege? (BCrypt para contrasenas, SECRET_KEY para la sesion, HTTPS para transporte)

## Que se implemento

Este paso agrega autenticacion completa al proyecto:

- **Login** con email y contrasena (encriptada con BCrypt)
- **Control de acceso por roles**: cada usuario tiene roles, cada rol tiene rutas permitidas
- **Cambio de contrasena** con validacion de seguridad
- **Recuperacion de contrasena** con envio de temporal por correo

---

## Archivos creados

```
FrontFlaskTutorial/
├── middleware/
│   └── auth_middleware.py         <- Intercepta cada request y verifica permisos
├── services/
│   ├── auth_service.py            <- Logica de login, roles, rutas, contrasenas
│   └── email_service.py           <- Envio de correos SMTP
├── routes/
│   └── auth.py                    <- Rutas: /login, /logout, /cambiar, /recuperar
└── templates/pages/
    ├── login.html                 <- Formulario de login
    ├── cambiar_contrasena.html    <- Formulario cambio de contrasena
    ├── recuperar_contrasena.html  <- Formulario recuperacion
    └── sin_acceso.html            <- Pagina error 403 (sin permisos)
```

---

## Tablas necesarias en la base de datos

Ejecute este SQL en PostgreSQL (en orden):

```sql
-- 1. Tabla de usuarios
CREATE TABLE usuario (
    email VARCHAR(200) PRIMARY KEY,
    contrasena VARCHAR(200) NOT NULL,
    nombre VARCHAR(200) DEFAULT '',
    debe_cambiar_contrasena BOOLEAN DEFAULT false
);

-- 2. Tabla de roles
CREATE TABLE rol (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL
);

-- 3. Tabla intermedia: que roles tiene cada usuario
CREATE TABLE rol_usuario (
    id SERIAL PRIMARY KEY,
    fkemail VARCHAR(200) REFERENCES usuario(email),
    fkidrol INTEGER REFERENCES rol(id)
);

-- 4. Tabla de rutas del sistema (paginas/endpoints)
CREATE TABLE ruta (
    id SERIAL PRIMARY KEY,
    ruta VARCHAR(200) NOT NULL,
    descripcion TEXT DEFAULT ''
);

-- 5. Tabla intermedia: que rutas puede acceder cada rol
CREATE TABLE rutarol (
    id SERIAL PRIMARY KEY,
    fkidrol INTEGER REFERENCES rol(id),
    fkidruta INTEGER REFERENCES ruta(id),
    fkruta VARCHAR(200) DEFAULT ''
);
```

### Datos iniciales de ejemplo

```sql
-- Crear un rol administrador
INSERT INTO rol (nombre) VALUES ('Administrador');

-- Crear un usuario con contrasena "Admin123" (texto plano, la API la encripta)
-- IMPORTANTE: No insertar directamente. Usar la API con ?encriptar=contrasena:
-- POST http://localhost:5035/api/usuario?encriptar=contrasena
-- Body: {"email": "admin@empresa.com", "contrasena": "Admin123", "nombre": "Administrador"}

-- Asignar rol al usuario
INSERT INTO rol_usuario (fkemail, fkidrol) VALUES ('admin@empresa.com', 1);
```

---

## Diagrama de relaciones

```
  usuario ──< rol_usuario >── rol ──< rutarol >── ruta
  (email)    (fkemail,       (id,    (fkidrol,    (id,
              fkidrol)        nombre)  fkidruta,    ruta,
                                       fkruta)      descripcion)
```

Ejemplo:
- El usuario "juan@mail.com" tiene rol "Vendedor" (id=2)
- El rol "Vendedor" tiene acceso a las rutas "/producto" y "/cliente"
- Entonces juan@mail.com puede acceder a /producto y /cliente
- Si intenta acceder a /factura, ve la pagina "Acceso Denegado" (403)

---

## Flujo de autenticacion

```
  1. Usuario abre http://localhost:5300
  2. Middleware detecta: no hay sesion → redirige a /login
  3. Usuario escribe email y contrasena → POST /login
  4. Flask envia credenciales a API C# (POST /api/autenticacion/token)
  5. API verifica contrasena con BCrypt → retorna token JWT
  6. Flask consulta roles del usuario (GET /api/rol_usuario + /api/rol)
  7. Flask consulta rutas permitidas (GET /api/rutarol)
  8. Todo se guarda en la sesion (cookie encriptada)
  9. Usuario es redirigido al inicio (/)
 10. En cada pagina que visita, el middleware verifica:
     - ¿Tiene sesion? → si no, redirige a /login
     - ¿La ruta esta en sus rutas_permitidas? → si no, muestra 403
```

---

## Que es BCrypt y por que se usa

BCrypt es un algoritmo de encriptacion de contrasenas **irreversible** (hash).

**Sin BCrypt** (inseguro):
```
Base de datos: email="juan@mail.com", contrasena="MiClave123"
→ Si alguien accede a la BD, ve todas las contrasenas en texto plano.
```

**Con BCrypt** (seguro):
```
Base de datos: email="juan@mail.com", contrasena="$2a$12$LJ3m4ys1Z..."
→ Si alguien accede a la BD, solo ve hashes incomprensibles.
→ No se puede obtener "MiClave123" a partir del hash.
→ Solo se puede verificar: "¿MiClave123 genera este hash?" → Si/No
```

La API generica C# maneja BCrypt automaticamente:
- Al crear/actualizar con `?encriptar=contrasena`, encripta con BCrypt
- Al autenticar con `/api/autenticacion/token`, verifica con BCrypt

---

## Configurar Gmail para envio de correos (SMTP)

Para que la recuperacion de contrasena envie correos, se necesita configurar SMTP en `config.py`. Aqui se explica paso a paso con Gmail.

### Paso 1: Activar verificacion en 2 pasos

1. Ir a [https://myaccount.google.com/security](https://myaccount.google.com/security)
2. En la seccion **"Como inicias sesion en Google"**, buscar **"Verificacion en 2 pasos"**
3. Si dice "Desactivada", hacer clic y seguir los pasos para activarla
4. Google pedira un numero de telefono para enviar codigos de verificacion
5. Completar la configuracion

> **¿Por que?** Google no permite usar App Passwords sin verificacion en 2 pasos.
> Es un requisito de seguridad obligatorio.

### Paso 2: Crear una App Password (contrasena de aplicacion)

1. Ir a [https://myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
   - Si el link no funciona, buscar en Google: "Google App Passwords"
   - O ir a: Google Account → Security → 2-Step Verification → App passwords
2. En **"Nombre de la app"**, escribir: `FlaskLogin` (o cualquier nombre descriptivo)
3. Hacer clic en **"Crear"**
4. Google mostrara una contrasena de 16 caracteres, algo como: `abcd efgh ijkl mnop`
5. **Copiarla inmediatamente** (solo se muestra una vez)
6. Quitar los espacios: `abcdefghijklmnop`

> **IMPORTANTE**: Esta NO es la contrasena normal de Gmail.
> Es una contrasena especial que solo sirve para aplicaciones externas.
> La contrasena normal de Gmail NO funciona para SMTP.

### Paso 3: Configurar config.py

Abrir `config.py` y llenar las variables SMTP:

```python
# SMTP (configurar para recuperacion de contrasena)
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "tucuenta@gmail.com"        # Tu email de Gmail
SMTP_PASS = "abcdefghijklmnop"          # La App Password (16 chars, sin espacios)
SMTP_FROM = "tucuenta@gmail.com"        # Mismo email (remitente)
```

### Paso 4: Probar

1. Ejecutar la aplicacion: `python app.py`
2. Ir a `http://localhost:5300/recuperar-contrasena`
3. Ingresar un email que exista en la tabla `usuario`
4. Si todo esta bien, el usuario recibira un correo con la contrasena temporal

### Si NO quiere configurar SMTP

La recuperacion de contrasena funciona **sin SMTP**, pero:
- La contrasena temporal se cambia en la BD (si funciona)
- El correo NO se envia (muestra un warning: "no se pudo enviar el correo")
- El administrador debe comunicar la contrasena temporal manualmente al usuario

### Problemas comunes

| Problema | Solucion |
|----------|----------|
| "App passwords not available" | Activar verificacion en 2 pasos primero |
| "Username and Password not accepted" | Usar App Password, NO la contrasena normal de Gmail |
| "SMTP no configurado" | Llenar SMTP_USER y SMTP_PASS en config.py |
| "Connection refused" | Verificar que el firewall no bloquee el puerto 587 |
| No llega el correo | Revisar la carpeta de spam del destinatario |

### Alternativas a Gmail

| Proveedor | SMTP_HOST | SMTP_PORT | Notas |
|-----------|-----------|-----------|-------|
| Gmail | smtp.gmail.com | 587 | Requiere App Password |
| Outlook/Hotmail | smtp-mail.outlook.com | 587 | Contrasena normal funciona |
| Yahoo | smtp.mail.yahoo.com | 587 | Requiere App Password |
| Mailtrap (pruebas) | sandbox.smtp.mailtrap.io | 587 | Gratis para desarrollo |

---

## Probar el login

1. Asegurese de que la API C# este corriendo en el puerto 5035
2. Asegurese de que las 5 tablas existan en la BD
3. Cree un usuario via la API (con encriptacion):
   ```
   POST http://localhost:5035/api/usuario?encriptar=contrasena
   Body: {"email": "admin@test.com", "contrasena": "Admin123", "nombre": "Admin"}
   ```
4. Cree un rol y asignelo:
   ```
   POST http://localhost:5035/api/rol
   Body: {"nombre": "Administrador"}

   POST http://localhost:5035/api/rol_usuario
   Body: {"fkemail": "admin@test.com", "fkidrol": 1}
   ```
5. Ejecute Flask: `python app.py`
6. Abra `http://localhost:5300` → deberia redirigir a `/login`
7. Ingrese `admin@test.com` / `Admin123` → deberia entrar
