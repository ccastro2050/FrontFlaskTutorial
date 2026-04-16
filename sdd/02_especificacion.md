# Etapa 2: Especificacion

> Segun [Spec-Kit de GitHub](https://github.com/github/spec-kit): la especificacion
> (`/speckit.specify`) documenta QUE construir y POR QUE, sin enfocarse en tecnologia.
> Se genera `spec.md` con historias de usuario y requisitos funcionales.
> "Se comienza con una idea, a menudo vaga, que evoluciona hacia un documento
> de requisitos comprensivo."
>
> Referencia: [spec-driven.md](https://github.com/github/spec-kit/blob/main/spec-driven.md)

---

## 1. Problema que resuelve

Los estudiantes de Diseno de Software necesitan aprender a construir un frontend web completo que consuma una API REST, con autenticacion, control de acceso, CRUD de tablas, y buenas practicas de desarrollo colaborativo. No existe un tutorial paso a paso que:

- Funcione con cualquier base de datos (no hardcodee nombres de columnas)
- Enseñe seguridad real (BCrypt + JWT + sesion)
- Permita trabajo colaborativo con Git (3 estudiantes, ramas, merges)
- Sea replicable en otros frameworks (Blazor, Java, PHP, React)

## 2. Para quien va dirigido

| Audiencia | Nivel | Que saben | Que no saben |
|-----------|-------|-----------|--------------|
| Estudiantes universitarios | Intermedio | Python basico, HTML, BD relacional | Flask, Jinja2, APIs REST, JWT, BCrypt |
| Profesor | Avanzado | Todo lo anterior + el API generica | N/A (es quien evalua) |

## 3. Que se construye

Un **frontend web completo** en Flask que:

### 3.1 Funcionalidades principales

| # | Funcionalidad | Descripcion | Tablas involucradas |
|---|---------------|-------------|---------------------|
| 1 | CRUD generico | Listar, crear, editar, eliminar registros de cualquier tabla | producto, persona, empresa, cliente, vendedor, usuario, rol, ruta |
| 2 | Login | Autenticacion con email + contrasena (BCrypt via API) | usuario |
| 3 | Control de acceso | Roles y rutas permitidas por rol, verificacion en cada request | rol, rol_usuario, ruta, rutarol |
| 4 | Cambiar contrasena | Con validacion (6 chars, mayuscula, numero) | usuario |
| 5 | Recuperar contrasena | Genera temporal, envia por SMTP, fuerza cambio | usuario |
| 6 | Navegacion | Sidebar con menu colapsable, layout base Bootstrap 5 | N/A |
| 7 | Factura maestro-detalle | Formulario con cabecera + lineas de detalle dinamicas | factura, productosporfactura |
| 8 | Descubrimiento dinamico | PKs y FKs se descubren de la API, no se hardcodean | Todas |

### 3.2 Modelo de datos (tablas de la BD)

```
┌──────────┐     ┌──────────────┐     ┌──────┐     ┌──────────┐     ┌──────┐
│ usuario  │──<──│ rol_usuario  │──>──│ rol  │──<──│ rutarol  │──>──│ ruta │
│ email PK │     │ fkemail      │     │ id   │     │ fkidrol  │     │ id   │
│ contrase │     │ fkidrol      │     │ nomb │     │ fkidruta │     │ ruta │
└──────────┘     └──────────────┘     └──────┘     └──────────┘     └──────┘

┌──────────┐     ┌──────────┐     ┌──────────┐
│ persona  │──<──│ cliente  │──>──│ empresa  │
│ codigo   │     │ fkcodper │     │ codigo   │
└──────────┘     │ fkcodemp │     └──────────┘
                 └──────────┘

┌──────────┐     ┌──────────┐     ┌──────────────────┐
│ vendedor │     │ factura  │──<──│productosporfactura│
│ codigo   │     │ numfact  │     │ fknumfact         │
└──────────┘     │ fkcodven │     │ fkcodprod         │
                 │ fkcodcli │     └──────────────────┘
                 └──────────┘

┌──────────┐
│ producto │
│ codigo   │
│ precio   │
└──────────┘
```

### 3.3 Modelo Entidad-Relacion (ER) detallado

> El modelo ER define las entidades (tablas), sus atributos (columnas),
> las relaciones entre ellas (FKs) y las restricciones (PKs, NOT NULL, UNIQUE).
> Es la base para el diseno de la BD.

#### Normalizacion aplicada

| Forma Normal | Que exige | Cumple? | Ejemplo |
|-------------|-----------|---------|---------|
| **1FN** | Valores atomicos, sin grupos repetidos | Si | Cada columna tiene un solo valor, no hay arrays |
| **2FN** | Todo atributo depende de TODA la PK | Si | En `productosporfactura`, cantidad depende de (fknumfact + fkcodprod), no solo de uno |
| **3FN** | No hay dependencias transitivas | Si | En `cliente`, el nombre de la persona NO se duplica — se accede via FK a `persona` |

#### Tabla de entidades y atributos

**Entidades de negocio:**

| Entidad | PK | Atributos | Tipo | NOT NULL | Descripcion |
|---------|-----|-----------|------|----------|-------------|
| **producto** | codigo (varchar) | nombre | varchar | si | Nombre del producto |
| | | precio | decimal | si | Precio unitario |
| | | existencia | integer | no | Cantidad en stock |
| **persona** | codigo (varchar) | nombre | varchar | si | Nombre completo |
| | | telefono | varchar | no | Telefono de contacto |
| | | direccion | varchar | no | Direccion fisica |
| **empresa** | codigo (varchar) | nombre | varchar | si | Razon social |
| | | nit | varchar | no | Numero tributario |
| **cliente** | id (serial) | credito | decimal | si | Limite de credito |
| | | fkcodpersona | varchar FK | si | -> persona.codigo |
| | | fkcodempresa | varchar FK | no | -> empresa.codigo |
| **vendedor** | codigo (varchar) | nombre | varchar | si | Nombre del vendedor |
| | | comision | decimal | no | Porcentaje comision |
| **factura** | numfactura (serial) | fecha | timestamp | si | Fecha de emision |
| | | total | decimal | si | Total de la factura |
| | | fkcodvendedor | varchar FK | si | -> vendedor.codigo |
| | | fkcodcliente | integer FK | si | -> cliente.id |
| **productosporfactura** | id (serial) | cantidad | integer | si | Unidades vendidas |
| | | precio | decimal | si | Precio al momento de la venta |
| | | fknumfact | integer FK | si | -> factura.numfactura |
| | | fkcodprod | varchar FK | si | -> producto.codigo |

**Entidades de seguridad:**

| Entidad | PK | Atributos | Tipo | NOT NULL | Descripcion |
|---------|-----|-----------|------|----------|-------------|
| **usuario** | email (varchar) | contrasena | varchar | si | Hash BCrypt (irreversible) |
| | | nombre | varchar | no | Nombre para mostrar |
| | | debe_cambiar_contrasena | boolean | no | Forzar cambio en proximo login |
| **rol** | id (serial) | nombre | varchar | si | Nombre del rol (Administrador, etc) |
| **rol_usuario** | id (serial) | fkemail | varchar FK | si | -> usuario.email |
| | | fkidrol | integer FK | si | -> rol.id |
| **ruta** | id (serial) | ruta | varchar | si | Path de la pagina (/producto) |
| | | descripcion | text | no | Descripcion de la pagina |
| **rutarol** | id (serial) | fkidrol | integer FK | si | -> rol.id |
| | | fkidruta | integer FK | si | -> ruta.id |

#### Cardinalidad de las relaciones

| Relacion | Tipo | Lectura | Tabla intermedia |
|----------|------|---------|-----------------|
| persona <-> cliente | 1:N | Una persona puede ser 0 o N clientes | No (FK directo) |
| empresa <-> cliente | 1:N | Una empresa puede tener 0 o N clientes | No (FK directo) |
| vendedor <-> factura | 1:N | Un vendedor tiene 0 o N facturas | No (FK directo) |
| cliente <-> factura | 1:N | Un cliente tiene 0 o N facturas | No (FK directo) |
| factura <-> producto | N:M | Una factura tiene N productos, un producto aparece en M facturas | Si: `productosporfactura` |
| usuario <-> rol | N:M | Un usuario tiene N roles, un rol tiene N usuarios | Si: `rol_usuario` |
| rol <-> ruta | N:M | Un rol accede a N rutas, una ruta la acceden N roles | Si: `rutarol` |

#### Integridad referencial

```
ON DELETE: Todas las FKs usan NO ACTION (no se puede borrar un registro
           que tenga hijos). La API devuelve error si se intenta.

ON UPDATE: NO ACTION. Si se cambia una PK, los FKs no se actualizan
           automaticamente (se debe actualizar manualmente).

Consecuencia practica:
  - No se puede borrar un vendedor que tenga facturas
  - No se puede borrar un rol que tenga usuarios asignados
  - No se puede borrar una ruta que este asignada a un rol
```

### 3.4 Flujos de usuario

#### Flujo 1: Login

```
Usuario abre app -> Middleware detecta sin sesion -> Redirect /login
-> Escribe email + contrasena -> POST /login
-> API verifica BCrypt -> Genera JWT -> Devuelve token
-> Cargar roles y rutas (1 SQL via ConsultasController)
-> Guardar en sesion Flask -> Redirect /
```

#### Flujo 2: CRUD (listar, crear, editar, eliminar)

```
Usuario navega a /producto -> Middleware verifica sesion + ruta permitida
-> ApiService.listar("producto") con JWT en header
-> API devuelve datos -> Jinja2 renderiza tabla HTML
-> Usuario llena formulario -> POST /producto/crear
-> ApiService.crear("producto", datos) con JWT -> API inserta en BD
-> Flash "Registro creado" -> Redirect /producto
```

#### Flujo 3: Factura maestro-detalle

```
Usuario navega a /factura -> Lista facturas existentes
-> Clic "Nueva factura" -> Formulario con:
   - Cabecera: vendedor (select FK), cliente (select FK), fecha
   - Detalle: tabla dinamica con producto (select FK), cantidad, precio
   - JavaScript agrega/elimina filas de detalle
-> POST /factura/crear -> Crea cabecera + detalles en la API
```

## 4. Que NO se construye (exclusiones explicitas)

| Excluido | Razon |
|----------|-------|
| API REST | Ya existe (ApiGenericaCsharp) |
| Base de datos | Ya existe (PostgreSQL) |
| Registro de usuarios | Los crea el admin via CRUD de usuario |
| Panel de administracion avanzado | Fuera del alcance del tutorial |
| Internacionalizacion (i18n) | Complejidad innecesaria para el tutorial |
| Tests automatizados | Se prueban manualmente (es un tutorial) |
| Deploy a produccion | Se ejecuta localmente (`python app.py`) |
| Notificaciones en tiempo real | Fuera del alcance |

## 5. Criterios de aceptacion

### Para cada CRUD

- [ ] Listar registros en tabla HTML con todos los campos
- [ ] Crear registro con formulario (tipos HTML correctos por tipo de dato)
- [ ] Editar registro (formulario prellenado con datos actuales)
- [ ] Eliminar registro con confirmacion
- [ ] Selects para campos FK (cargados desde la API)
- [ ] Mensajes flash de exito/error despues de cada operacion

### Para login y seguridad

- [ ] Login con email + contrasena verificada con BCrypt
- [ ] JWT capturado y enviado en cada peticion a la API
- [ ] Roles cargados desde la BD (no hardcodeados)
- [ ] Rutas permitidas verificadas en CADA request (middleware)
- [ ] Usuario sin roles -> rechazado con mensaje claro
- [ ] Ruta no permitida -> pagina 403 "Acceso Denegado"
- [ ] Cambiar contrasena con validacion (6 chars, mayuscula, numero)
- [ ] Recuperar contrasena con email SMTP
- [ ] Sesion persiste al navegar, se pierde al cerrar navegador

### Para trabajo colaborativo

- [ ] Cada estudiante trabaja en su rama feature/
- [ ] Merge a main sin conflictos (o resueltos en la rama)
- [ ] Cada paso tiene su commit descriptivo
- [ ] El proyecto arranca con `python app.py` despues de cada merge

## 6. Metricas de exito

| Metrica | Valor esperado |
|---------|----------------|
| Tablas CRUD funcionando | 10+ |
| Tiempo de login (con ConsultasController) | < 2 segundos |
| Estudiantes que completan el tutorial | 3/3 |
| El proyecto compila y corre despues de merge | Si |
| Cada paso tiene documentacion (.md) | Si (Paso0 a Paso12) |
