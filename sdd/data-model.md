# Modelo de Datos - FrontFlaskTutorial

> Según [Spec-Kit de GitHub](https://github.com/github/spec-kit), cada feature puede
> tener un archivo `data-model.md` dedicado con el esquema detallado de entidades.
> Este archivo contiene el SQL completo para crear todas las tablas del proyecto.
>
> Referencia: [estructura .specify/specs/{feature}/data-model.md](https://github.com/github/spec-kit)

---

## 1. Diagrama Entidad-Relación (ER)

```
                           SEGURIDAD
    ┌──────────┐     ┌──────────────┐     ┌──────┐     ┌──────────┐     ┌──────┐
    │ usuario  │──<──│ rol_usuario  │──>──│ rol  │──<──│ rutarol  │──>──│ ruta │
    │ email PK │     │ fkemail  FK  │     │ id PK│     │ fkidrol  │     │ id PK│
    │ contrase │     │ fkidrol  FK  │     │ nomb │     │ fkidruta │     │ ruta │
    │ nombre   │     └──────────────┘     └──────┘     └──────────┘     │ desc │
    │ debe_cam │           N:M                              N:M         └──────┘
    └──────────┘

                            NEGOCIO
    ┌──────────┐     ┌──────────┐     ┌──────────┐
    │ persona  │──<──│ cliente  │──>──│ empresa  │
    │ codigo PK│ 1:N │ id PK    │ N:1 │ codigo PK│
    │ nombre   │     │ credito  │     │ nombre   │
    │ telefono │     │ fkcodper │     │ nit      │
    │ direccion│     │ fkcodemp │     │ direccion│
    └──────────┘     └──────────┘     └──────────┘

    ┌──────────┐     ┌──────────────┐     ┌──────────────────┐     ┌──────────┐
    │ vendedor │──<──│   factura    │──<──│productosporfactur│──>──│ producto │
    │ codigo PK│ 1:N │ numfact PK  │ 1:N │ id PK            │ N:1 │ codigo PK│
    │ nombre   │     │ fecha       │     │ cantidad         │     │ nombre   │
    │ comision │     │ total       │     │ precio           │     │ precio   │
    └──────────┘     │ fkcodven FK │     │ fknumfact FK     │     │ existenc │
                     │ fkcodcli FK │     │ fkcodprod FK     │     └──────────┘
                     └──────────────┘     └──────────────────┘
```

## 2. SQL completo para PostgreSQL

```sql
-- ═══════════════════════════════════════════════════════
-- TABLAS DE NEGOCIO
-- ═══════════════════════════════════════════════════════

-- Producto: articulos que se venden
CREATE TABLE producto (
    codigo VARCHAR(20) PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL,
    precio DECIMAL(18,2) NOT NULL DEFAULT 0,
    existencia INTEGER DEFAULT 0
);

-- Persona: datos de personas naturales
CREATE TABLE persona (
    codigo VARCHAR(20) PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL,
    telefono VARCHAR(50) DEFAULT '',
    direccion VARCHAR(300) DEFAULT ''
);

-- Empresa: datos de personas juridicas
CREATE TABLE empresa (
    codigo VARCHAR(20) PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL,
    nit VARCHAR(50) DEFAULT '',
    direccion VARCHAR(300) DEFAULT ''
);

-- Cliente: puede ser persona natural (fkcodpersona) o juridica (fkcodempresa)
-- fkcodempresa es nullable: si es persona natural, no tiene empresa
CREATE TABLE cliente (
    id SERIAL PRIMARY KEY,
    credito DECIMAL(18,2) NOT NULL DEFAULT 0,
    fkcodpersona VARCHAR(20) NOT NULL REFERENCES persona(codigo),
    fkcodempresa VARCHAR(20) REFERENCES empresa(codigo)  -- nullable
);

-- Vendedor: personas que venden
CREATE TABLE vendedor (
    codigo VARCHAR(20) PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL,
    comision DECIMAL(5,2) DEFAULT 0
);

-- Factura: cabecera de la factura (maestro)
CREATE TABLE factura (
    numfactura SERIAL PRIMARY KEY,
    fecha TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    total DECIMAL(18,2) NOT NULL DEFAULT 0,
    fkcodvendedor VARCHAR(20) NOT NULL REFERENCES vendedor(codigo),
    fkcodcliente INTEGER NOT NULL REFERENCES cliente(id)
);

-- ProductosPorFactura: detalle de la factura (detalle)
-- Guarda el precio al momento de la venta (puede cambiar en el futuro)
CREATE TABLE productosporfactura (
    id SERIAL PRIMARY KEY,
    cantidad INTEGER NOT NULL DEFAULT 1,
    precio DECIMAL(18,2) NOT NULL,  -- precio al momento de la venta
    fknumfact INTEGER NOT NULL REFERENCES factura(numfactura),
    fkcodprod VARCHAR(20) NOT NULL REFERENCES producto(codigo)
);

-- ═══════════════════════════════════════════════════════
-- TABLAS DE SEGURIDAD (autenticacion y autorizacion)
-- ═══════════════════════════════════════════════════════

-- Usuario: credenciales de acceso
-- contrasena se guarda como hash BCrypt (irreversible)
CREATE TABLE usuario (
    email VARCHAR(200) PRIMARY KEY,
    contrasena VARCHAR(200) NOT NULL,  -- hash BCrypt, NUNCA texto plano
    nombre VARCHAR(200) DEFAULT '',
    debe_cambiar_contrasena BOOLEAN DEFAULT false
);

-- Rol: tipos de usuario del sistema
CREATE TABLE rol (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL  -- ej: "Administrador", "Vendedor", "Contador"
);

-- Rol_usuario: asigna roles a usuarios (relacion N:M)
-- Un usuario puede tener varios roles
CREATE TABLE rol_usuario (
    id SERIAL PRIMARY KEY,
    fkemail VARCHAR(200) NOT NULL REFERENCES usuario(email),
    fkidrol INTEGER NOT NULL REFERENCES rol(id)
);

-- Ruta: paginas/endpoints del sistema
CREATE TABLE ruta (
    id SERIAL PRIMARY KEY,
    ruta VARCHAR(200) NOT NULL,  -- ej: "/producto", "/factura"
    descripcion TEXT DEFAULT ''
);

-- Rutarol: define que paginas puede acceder cada rol (relacion N:M)
CREATE TABLE rutarol (
    id SERIAL PRIMARY KEY,
    fkidrol INTEGER NOT NULL REFERENCES rol(id),
    fkidruta INTEGER NOT NULL REFERENCES ruta(id)
);
```

## 3. SQL para SqlServer (equivalente)

```sql
-- Las diferencias con PostgreSQL:
--   SERIAL            -> INT IDENTITY(1,1)
--   BOOLEAN           -> BIT
--   TEXT               -> NVARCHAR(MAX)
--   VARCHAR            -> NVARCHAR
--   DECIMAL            -> DECIMAL (igual)
--   DEFAULT CURRENT_TIMESTAMP -> DEFAULT GETDATE()
--   REFERENCES         -> FOREIGN KEY ... REFERENCES (igual)

-- Ejemplo:
CREATE TABLE producto (
    codigo NVARCHAR(20) PRIMARY KEY,
    nombre NVARCHAR(200) NOT NULL,
    precio DECIMAL(18,2) NOT NULL DEFAULT 0,
    existencia INT DEFAULT 0
);
```

## 4. Datos iniciales de ejemplo

```sql
-- Roles del sistema
INSERT INTO rol (nombre) VALUES ('Administrador');
INSERT INTO rol (nombre) VALUES ('Vendedor');
INSERT INTO rol (nombre) VALUES ('Cajero');
INSERT INTO rol (nombre) VALUES ('Contador');
INSERT INTO rol (nombre) VALUES ('Cliente');

-- Usuario administrador (contrasena se crea via API con BCrypt):
-- POST http://localhost:5035/api/usuario?camposEncriptar=contrasena
-- Body: {"email": "admin@test.com", "contrasena": "Admin123"}

-- Asignar rol administrador
INSERT INTO rol_usuario (fkemail, fkidrol) VALUES ('admin@test.com', 1);

-- Rutas del sistema
INSERT INTO ruta (ruta, descripcion) VALUES ('/home', 'Pagina inicio');
INSERT INTO ruta (ruta, descripcion) VALUES ('/producto', 'Gestion de productos');
INSERT INTO ruta (ruta, descripcion) VALUES ('/factura', 'Gestion de facturas');
INSERT INTO ruta (ruta, descripcion) VALUES ('/cliente', 'Gestion de clientes');
INSERT INTO ruta (ruta, descripcion) VALUES ('/usuario', 'Gestion de usuarios');

-- Asignar todas las rutas al rol Administrador
INSERT INTO rutarol (fkidrol, fkidruta) VALUES (1, 1);  -- admin -> /home
INSERT INTO rutarol (fkidrol, fkidruta) VALUES (1, 2);  -- admin -> /producto
INSERT INTO rutarol (fkidrol, fkidruta) VALUES (1, 3);  -- admin -> /factura
INSERT INTO rutarol (fkidrol, fkidruta) VALUES (1, 4);  -- admin -> /cliente
INSERT INTO rutarol (fkidrol, fkidruta) VALUES (1, 5);  -- admin -> /usuario
```

## 5. Diccionario de datos

| Tipo de dato | PostgreSQL | SqlServer | Python | HTML input |
|-------------|-----------|-----------|--------|------------|
| Texto corto | VARCHAR(N) | NVARCHAR(N) | str | type="text" |
| Texto largo | TEXT | NVARCHAR(MAX) | str | textarea |
| Entero | INTEGER | INT | int | type="number" |
| Decimal | DECIMAL(18,2) | DECIMAL(18,2) | float | type="number" step="0.01" |
| Booleano | BOOLEAN | BIT | bool | type="checkbox" |
| Fecha/hora | TIMESTAMP | DATETIME2 | datetime | type="datetime-local" |
| Auto-incremento | SERIAL | IDENTITY(1,1) | (generado por BD) | (oculto) |
| Email | VARCHAR(200) | NVARCHAR(200) | str | type="email" |
| Contrasena | VARCHAR(200) | NVARCHAR(200) | str (hash) | type="password" |

---

## Referencias

- Formato data-model: [Spec-Kit estructura de specs](https://github.com/github/spec-kit)
- Normalización: 02_especificacion.md, sección 3.3
- ACID: 01_constitucion.md, Artículo VIII
- Compatibilidad Postgres/SqlServer: 03_clarificacion.md, sección 4
