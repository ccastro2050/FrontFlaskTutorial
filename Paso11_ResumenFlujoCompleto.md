# Paso 11 — Resumen del Flujo Completo

Este documento es un resumen paso a paso de **todo** lo que hizo cada estudiante a lo largo del tutorial. Sirve como hoja de referencia ("cheat sheet") para repasar el proyecto completo.

**Tecnologia:** Flask, Python 3, Jinja2
**API:** ApiGenericaCsharp en `http://localhost:5035`
**Comando para ejecutar:** `python app.py` (puerto 5300)
**Entorno virtual:** `python -m venv venv` + `venv\Scripts\activate` + `pip install -r requirements.txt`

---

## Estudiante 1 (Administrador / Scrum Master)

Estudiante 1 es el administrador del repositorio. Crea el proyecto, invita a los colaboradores, revisa y aprueba los PRs de los demas, y hace merge a main.

---

### Paso 0 — Plan de Desarrollo

No requiere codigo. Se revisa el plan de desarrollo, se asignan las historias de usuario y se definen las convenciones de trabajo (ramas, commits, PRs).

---

### Paso 3 — Crear el Proyecto y Configurar GitHub

**Rama:** trabaja directamente en `main` (es el commit inicial)

**Archivos creados:** app.py, config.py, requirements.txt, .gitignore, routes/__init__.py, services/__init__.py

```powershell
# --- Crear el proyecto ---
cd C:\Users\TU_USUARIO\Desktop\proyectoscsharp                  # ir a la carpeta de proyectos
mkdir FrontFlaskTutorial                                          # crear carpeta del proyecto
cd FrontFlaskTutorial                                             # entrar al proyecto

# --- Crear entorno virtual e instalar dependencias ---
python -m venv venv                                               # crear entorno virtual
venv\Scripts\activate                                             # activar entorno virtual
pip install flask requests                                        # instalar Flask y requests
pip freeze > requirements.txt                                     # guardar dependencias

# --- Crear estructura de carpetas ---
mkdir routes, services, templates, static, scripts_bds            # carpetas principales
mkdir templates\layout, templates\components, templates\pages, static\css  # subcarpetas
New-Item routes\__init__.py                                       # init del paquete routes
New-Item services\__init__.py                                     # init del paquete services

# --- Crear archivos config.py, app.py y .gitignore ---
# config.py: API_BASE_URL y SECRET_KEY
# app.py: crea Flask, registra Blueprints
# .gitignore: excluye venv/, __pycache__/, .pyc

# --- Verificar que funciona ---
python app.py                                                     # debe arrancar en http://localhost:5300

# --- Inicializar Git y subir a GitHub ---
git init                                                          # inicializar repositorio git
git add .                                                         # agregar todos los archivos al staging
git commit -m "Proyecto Flask inicial"                            # primer commit
git remote add origin https://github.com/TU_USUARIO/FrontFlaskTutorial.git  # conectar con GitHub
git branch -M main                                                # renombrar rama a main
git push -u origin main                                           # subir a GitHub

# --- Invitar colaboradores ---
# En GitHub: Settings > Collaborators > Add people
# Agregar a Estudiante 2 y Estudiante 3
```

---

### Paso 4 — Conexion a la API y ApiService

**Rama:** `api-service`

**Archivos creados/modificados:**
- `services/api_service.py` (NUEVO)

```powershell
git checkout main                          # volver a la rama principal
git pull                                   # descargar ultimos cambios
git checkout -b api-service                # crear rama para el ApiService

# --- Crear services/api_service.py ---
# Clase ApiService con metodos:
#   listar(tabla, limite)          → GET /api/{tabla}
#   crear(tabla, datos)            → POST /api/{tabla}
#   actualizar(tabla, clave, valor, datos) → PUT /api/{tabla}/{clave}/{valor}
#   eliminar(tabla, clave, valor)  → DELETE /api/{tabla}/{clave}/{valor}
# Usa la libreria requests para las peticiones HTTP

# --- Verificar y subir ---
python -c "from services.api_service import ApiService; print('OK')"  # verificar que importa
git add .                                  # agregar cambios al staging
git commit -m "Agregar ApiService y configurar conexion a la API"     # commit
git push -u origin api-service             # subir rama a GitHub

# --- En GitHub: crear PR api-service -> main, aprobar y merge ---
```

---

### Paso 5 — Layout, Navegacion y Home

**Rama:** `layout-navegacion-home`

**Archivos creados:**
- `static/css/app.css` (NUEVO) — estilos del sidebar y responsive
- `templates/layout/base.html` (NUEVO) — template base con sidebar + contenido
- `templates/components/nav_menu.html` (NUEVO) — menu lateral
- `templates/pages/home.html` (NUEVO) — pagina de inicio con diagnostico
- `routes/home.py` (NUEVO) — Blueprint de Home

**Archivos modificados:**
- `app.py` (MODIFICADO) — registrar Blueprint de Home

```powershell
git checkout main                          # volver a la rama principal
git pull                                   # descargar ultimos cambios
git checkout -b layout-navegacion-home     # crear rama para layout y home

# --- Crear los archivos de layout, menu, home y CSS ---
# base.html: estructura HTML con Bootstrap, sidebar, mensajes flash, bloque content
# nav_menu.html: links a Home, Producto, Persona, Usuario, Empresa, Rol, Ruta
# home.html: titulo, tablas disponibles, info de conexion a la BD
# home.py: Blueprint con ruta GET / que consulta diagnostico de la API
# app.css: estilos del sidebar, responsive, iconos SVG

# --- Modificar app.py ---
# Agregar: from routes.home import bp as home_bp
# Agregar: app.register_blueprint(home_bp)

# --- Verificar y subir ---
python app.py                              # verificar que funciona en http://localhost:5300
git add .                                  # agregar cambios
git commit -m "Configurar layout, navegacion y pagina Home"       # commit
git push -u origin layout-navegacion-home  # subir rama

# --- En GitHub: crear PR layout-navegacion-home -> main, aprobar y merge ---
```

---

### Paso 6 — CRUD Producto

**Rama:** `crud-producto`

**Archivos creados:**
- `routes/producto.py` (NUEVO) — Blueprint con 4 rutas
- `templates/pages/producto.html` (NUEVO) — template con tabla y formulario

**Archivos modificados:**
- `app.py` (MODIFICADO) — registrar Blueprint de Producto

```powershell
git checkout main                          # volver a la rama principal
git pull                                   # descargar ultimos cambios
git checkout -b crud-producto              # crear rama para CRUD Producto

# --- Crear routes/producto.py ---
# Blueprint 'producto' con TABLA='producto', CLAVE='codigo'
# Rutas: GET /producto, POST /producto/crear, POST /producto/actualizar, POST /producto/eliminar
# Campos: codigo (str), nombre (str), stock (int), valorunitario (float)

# --- Crear templates/pages/producto.html ---
# Template con: boton nuevo, limite, formulario crear/editar, tabla con acciones
# Usa url_for('producto.index'), url_for('producto.crear'), etc.

# --- Modificar app.py ---
# Agregar: from routes.producto import bp as producto_bp
# Agregar: app.register_blueprint(producto_bp)

# --- Verificar y subir ---
python app.py                              # verificar en http://localhost:5300/producto
git add .                                  # agregar cambios
git commit -m "Agregar pagina CRUD Producto"                      # commit
git push -u origin crud-producto           # subir rama

# --- En GitHub: crear PR crud-producto -> main, aprobar y merge ---
```

---

### Paso 8 — CRUD Empresa

**Rama:** `crud-empresa`

**Archivos creados:**
- `routes/empresa.py` (NUEVO)
- `templates/pages/empresa.html` (NUEVO)

**Archivos modificados:**
- `app.py` (MODIFICADO)

```powershell
git checkout main                          # volver a la rama principal
git pull                                   # descargar ultimos cambios
git checkout -b crud-empresa               # crear rama para CRUD Empresa

# --- Crear routes/empresa.py y templates/pages/empresa.html ---
# Tabla simple con 2 campos: codigo (str), nombre (str)
# Misma estructura que Producto pero mas sencilla

# --- Verificar y subir ---
git add .                                  # agregar cambios
git commit -m "Agregar ruta y template CRUD Empresa"              # commit
git push -u origin crud-empresa            # subir rama

# --- En GitHub: crear PR crud-empresa -> main, aprobar y merge ---
# IMPORTANTE: hacer merge de Empresa ANTES que Cliente (Est2 depende de esta tabla)
```

---

### Paso 9 — CRUD Ruta

**Rama:** `crud-ruta`

**Archivos creados:**
- `routes/ruta.py` (NUEVO)
- `templates/pages/ruta.html` (NUEVO)

**Archivos modificados:**
- `app.py` (MODIFICADO)

```powershell
git checkout main                          # volver a la rama principal
git pull                                   # descargar ultimos cambios
git checkout -b crud-ruta                  # crear rama para CRUD Ruta

# --- Crear routes/ruta.py y templates/pages/ruta.html ---
# Campos: ruta (str, PK), descripcion (str)
# Blueprint se llama 'ruta_page' (no 'ruta') para no confundir con el campo
# En templates se usa url_for('ruta_page.index')

# --- Verificar y subir ---
git add .                                  # agregar cambios
git commit -m "Agregar ruta y template CRUD Ruta"                 # commit
git push -u origin crud-ruta               # subir rama

# --- En GitHub: crear PR crud-ruta -> main, aprobar y merge ---
```

---

### Paso 10 — Agregar ejecutar_sp a ApiService

**Rama:** `agregar-ejecutar-sp`

**Archivos modificados:**
- `services/api_service.py` (MODIFICADO) — agregar metodo ejecutar_sp

```powershell
git checkout main                          # volver a la rama principal
git pull                                   # descargar ultimos cambios
git checkout -b agregar-ejecutar-sp        # crear rama para ejecutar_sp

# --- Modificar services/api_service.py ---
# Agregar metodo ejecutar_sp(nombre_sp, parametros)
# Endpoint: POST /api/procedimientos/ejecutarsp
# Retorna: (bool exito, datos_o_mensaje)

# --- Verificar y subir ---
git add .                                  # agregar cambios
git commit -m "Agregar metodo ejecutar_sp a ApiService"           # commit
git push -u origin agregar-ejecutar-sp     # subir rama

# --- En GitHub: crear PR agregar-ejecutar-sp -> main, aprobar y merge ---
# IMPORTANTE: hacer merge ANTES de que Est2 suba su PR de Factura
```

---

## Estudiante 2

Estudiante 2 se enfoca en las tablas que tienen llaves foraneas y la factura (la pagina mas compleja).

---

### Paso 3 — Clonar el Repositorio

```powershell
# --- Aceptar invitacion ---
# En GitHub: ir a Notifications, aceptar invitacion al repositorio

# --- Clonar ---
cd C:\Users\TU_USUARIO\Desktop\proyectoscsharp                    # ir a la carpeta de proyectos
git clone https://github.com/USUARIO_EST1/FrontFlaskTutorial.git  # clonar el repositorio
cd FrontFlaskTutorial                                              # entrar al proyecto

# --- Crear entorno virtual e instalar dependencias ---
python -m venv venv                                                # crear entorno virtual
venv\Scripts\activate                                              # activar entorno virtual
pip install -r requirements.txt                                    # instalar dependencias

# --- Verificar ---
python app.py                                                      # verificar que funciona
```

---

### Paso 7 — CRUD Persona

**Rama:** `crud-persona`

**Archivos creados:**
- `routes/persona.py` (NUEVO)
- `templates/pages/persona.html` (NUEVO)

**Archivos modificados:**
- `app.py` (MODIFICADO) — registrar Blueprint

```powershell
git checkout main                          # volver a la rama principal
git pull                                   # descargar ultimos cambios
git checkout -b crud-persona               # crear rama para CRUD Persona

# --- Crear routes/persona.py y templates/pages/persona.html ---
# Campos: codigo (str), nombre (str), email (str), telefono (str)
# Misma estructura que Producto, cambian los campos

# --- Modificar app.py ---
# Agregar: from routes.persona import bp as persona_bp
# Agregar: app.register_blueprint(persona_bp)

# --- Verificar y subir ---
git add .                                  # agregar cambios
git commit -m "Agregar ruta y template CRUD Persona"              # commit
git push -u origin crud-persona            # subir rama

# --- En GitHub: crear PR crud-persona -> main ---
# Estudiante 1 revisa, aprueba y hace merge
```

---

### Paso 8 — CRUD Cliente (con llaves foraneas)

**Rama:** `crud-cliente`

**Depende de:** Empresa (Est1) y Persona (Est2) deben estar mergeados

**Archivos creados:**
- `routes/cliente.py` (NUEVO)
- `templates/pages/cliente.html` (NUEVO)

**Archivos modificados:**
- `app.py` (MODIFICADO)

```powershell
git checkout main                          # volver a la rama principal
git pull                                   # descargar ultimos cambios
git checkout -b crud-cliente               # crear rama para CRUD Cliente

# --- Crear routes/cliente.py ---
# Campos: id (int, auto), credito (float), fkcodpersona (FK), fkcodempresa (FK, opcional)
# Carga personas y empresas con api.listar('persona') y api.listar('empresa')
# Crea mapa_personas y mapa_empresas para mostrar nombres en la tabla

# --- Crear templates/pages/cliente.html ---
# Tiene <select> para persona (obligatorio) y empresa (opcional)
# El id no se envia al crear (lo genera la BD)

# --- Si Empresa aun no esta mergeada ---
git fetch origin                           # descargar cambios de GitHub sin aplicarlos
git merge origin/main                      # traer lo nuevo de main a esta rama

# --- Verificar y subir ---
git add .                                  # agregar cambios
git commit -m "Agregar ruta y template CRUD Cliente"              # commit
git push -u origin crud-cliente            # subir rama

# --- En GitHub: crear PR crud-cliente -> main ---
```

---

### Paso 9 — CRUD Vendedor (con llave foranea)

**Rama:** `crud-vendedor`

**Archivos creados:**
- `routes/vendedor.py` (NUEVO)
- `templates/pages/vendedor.html` (NUEVO)

**Archivos modificados:**
- `app.py` (MODIFICADO)

```powershell
git checkout main                          # volver a la rama principal
git pull                                   # descargar ultimos cambios
git checkout -b crud-vendedor              # crear rama para CRUD Vendedor

# --- Crear routes/vendedor.py y templates/pages/vendedor.html ---
# Campos: id (int, auto), carnet (str), direccion (str), fkcodpersona (FK)
# Carga personas para el select, mapa_personas para nombres en la tabla

# --- Verificar y subir ---
git add .                                  # agregar cambios
git commit -m "Agregar ruta y template CRUD Vendedor"             # commit
git push -u origin crud-vendedor           # subir rama

# --- En GitHub: crear PR crud-vendedor -> main ---
```

---

### Paso 10 — CRUD Factura (Maestro-Detalle con SPs)

**Rama:** `crud-factura`

**Depende de:** ejecutar_sp (Est1), Cliente (Est2), Vendedor (Est2) deben estar mergeados

**Archivos creados:**
- `routes/factura.py` (NUEVO)
- `templates/pages/factura.html` (NUEVO)

**Archivos modificados:**
- `app.py` (MODIFICADO)

```powershell
git checkout main                          # volver a la rama principal
git pull                                   # descargar ultimos cambios
git checkout -b crud-factura               # crear rama para Factura

# --- Si ejecutar_sp se mergeo despues de crear la rama ---
git fetch origin                           # descargar cambios de GitHub sin aplicarlos
git merge origin/main                      # traer ejecutar_sp a esta rama

# --- Crear routes/factura.py ---
# 6 rutas: index (listar), ver, nueva, crear, editar, actualizar, eliminar
# Usa api.ejecutar_sp() para llamar a los Stored Procedures
# SPs: sp_listar_facturas, sp_consultar_factura, sp_insertar_factura,
#       sp_actualizar_factura, sp_borrar_factura
# Carga clientes, vendedores, personas y productos para los selects
# Cruza cliente/vendedor con persona para obtener nombres

# --- Crear templates/pages/factura.html ---
# 3 vistas controladas por variable 'vista': listar, ver, formulario
# Vista listar: tabla con numero, cliente, vendedor, fecha, total, productos
# Vista ver: detalle de factura con tabla de productos
# Vista formulario: selects de cliente/vendedor + filas dinamicas de productos
# JavaScript: funcion agregarProducto() para agregar filas de productos

# --- Verificar y subir ---
git add .                                  # agregar cambios
git commit -m "Agregar pagina Factura con stored procedures"      # commit
git push -u origin crud-factura            # subir rama

# --- En GitHub: crear PR crud-factura -> main ---
```

---

## Estudiante 3

Estudiante 3 trabaja en las tablas mas simples y en tareas de soporte (NavMenu, Home).

---

### Paso 3 — Clonar el Repositorio

```powershell
# --- Aceptar invitacion ---
# En GitHub: ir a Notifications, aceptar invitacion al repositorio

# --- Clonar ---
cd C:\Users\TU_USUARIO\Desktop\proyectoscsharp                    # ir a la carpeta de proyectos
git clone https://github.com/USUARIO_EST1/FrontFlaskTutorial.git  # clonar el repositorio
cd FrontFlaskTutorial                                              # entrar al proyecto

# --- Crear entorno virtual e instalar dependencias ---
python -m venv venv                                                # crear entorno virtual
venv\Scripts\activate                                              # activar entorno virtual
pip install -r requirements.txt                                    # instalar dependencias

# --- Verificar ---
python app.py                                                      # verificar que funciona
```

---

### Paso 7 — CRUD Usuario

**Rama:** `crud-usuario`

**Archivos creados:**
- `routes/usuario.py` (NUEVO)
- `templates/pages/usuario.html` (NUEVO)

**Archivos modificados:**
- `app.py` (MODIFICADO)

```powershell
git checkout main                          # volver a la rama principal
git pull                                   # descargar ultimos cambios
git checkout -b crud-usuario               # crear rama para CRUD Usuario

# --- Crear routes/usuario.py y templates/pages/usuario.html ---
# Campos: email (str, PK), contrasena (str)
# Diferencia: clave primaria es 'email', no 'codigo'
# Input de contrasena usa type="password"

# --- Verificar y subir ---
git add .                                  # agregar cambios
git commit -m "Agregar ruta y template CRUD Usuario"              # commit
git push -u origin crud-usuario            # subir rama

# --- En GitHub: crear PR crud-usuario -> main ---
```

---

### Paso 8 — CRUD Rol

**Rama:** `crud-rol`

**Archivos creados:**
- `routes/rol.py` (NUEVO)
- `templates/pages/rol.html` (NUEVO)

**Archivos modificados:**
- `app.py` (MODIFICADO)

```powershell
git checkout main                          # volver a la rama principal
git pull                                   # descargar ultimos cambios
git checkout -b crud-rol                   # crear rama para CRUD Rol

# --- Crear routes/rol.py y templates/pages/rol.html ---
# Campos: id (int, PK), nombre (str)
# Diferencia: clave primaria es 'id' (int), no 'codigo' (str)
# Input de id usa type="number"

# --- Verificar y subir ---
git add .                                  # agregar cambios
git commit -m "Agregar ruta y template CRUD Rol"                  # commit
git push -u origin crud-rol                # subir rama

# --- En GitHub: crear PR crud-rol -> main ---
```

---

### Paso 9 — Actualizar NavMenu

**Rama:** `actualizar-navmenu`

**Archivos modificados:**
- `templates/components/nav_menu.html` (MODIFICADO)

```powershell
git checkout main                          # volver a la rama principal
git pull                                   # descargar ultimos cambios
git checkout -b actualizar-navmenu         # crear rama para actualizar el menu

# --- Modificar templates/components/nav_menu.html ---
# Agregar links a: Cliente, Vendedor, Facturas

# --- Verificar y subir ---
git add .                                  # agregar cambios
git commit -m "Agregar links de Cliente, Vendedor y Factura al menu"  # commit
git push -u origin actualizar-navmenu      # subir rama

# --- En GitHub: crear PR actualizar-navmenu -> main ---
```

---

### Paso 10 — Actualizar Home

**Rama:** `actualizar-home`

**Archivos modificados:**
- `templates/pages/home.html` (MODIFICADO)

```powershell
git checkout main                          # volver a la rama principal
git pull                                   # descargar ultimos cambios
git checkout -b actualizar-home            # crear rama para actualizar Home

# --- Modificar templates/pages/home.html ---
# Cambiar "Tablas disponibles: Producto, Persona, Usuario, Empresa, Rol, Ruta"
# Por: "Tablas disponibles: Producto, Persona, Usuario, Empresa, Rol, Ruta, Cliente, Vendedor, Factura"

# --- Verificar y subir ---
git add .                                  # agregar cambios
git commit -m "Actualizar Home con lista completa de tablas"      # commit
git push -u origin actualizar-home         # subir rama

# --- En GitHub: crear PR actualizar-home -> main ---
```

---

## Cronologia de Pull Requests

| # | Sprint | Paso | Rama | Descripcion | Responsable | Depende de |
|---|--------|------|------|-------------|-------------|------------|
| 1 | Sprint 2 | 4 | `api-service` | ApiService + conexion a la API | Est1 | - |
| 2 | Sprint 2 | 5 | `layout-navegacion-home` | Layout, NavMenu y Home | Est1 | PR #1 |
| 3 | Sprint 3 | 6 | `crud-producto` | CRUD Producto | Est1 | PR #2 |
| 4 | Sprint 4 | 7 | `crud-persona` | CRUD Persona | Est2 | PR #3 |
| 5 | Sprint 4 | 7 | `crud-usuario` | CRUD Usuario | Est3 | PR #3 |
| 6 | Sprint 5 | 8 | `crud-empresa` | CRUD Empresa | Est1 | PR #3 |
| 7 | Sprint 5 | 8 | `crud-rol` | CRUD Rol | Est3 | PR #3 |
| 8 | Sprint 5 | 8 | `crud-cliente` | CRUD Cliente (con FKs) | Est2 | PR #4, #6 |
| 9 | Sprint 6 | 9 | `crud-ruta` | CRUD Ruta | Est1 | - |
| 10 | Sprint 6 | 9 | `crud-vendedor` | CRUD Vendedor (con FK) | Est2 | PR #4 |
| 11 | Sprint 6 | 9 | `actualizar-navmenu` | NavMenu completo | Est3 | - |
| 12 | Sprint 7 | 10 | `agregar-ejecutar-sp` | ejecutar_sp en ApiService | Est1 | - |
| 13 | Sprint 7 | 10 | `actualizar-home` | Home actualizado | Est3 | - |
| 14 | Sprint 7 | 10 | `crud-factura` | Factura maestro-detalle | Est2 | PR #12 |

---

## Estado Final del Proyecto

### Estructura de archivos completa

```
FrontFlaskTutorial/
├── app.py                              ← Est1 (Paso 3) - punto de entrada, registro de Blueprints
├── config.py                           ← Est1 (Paso 3) - API_BASE_URL y SECRET_KEY
├── requirements.txt                    ← Est1 (Paso 3) - dependencias (Flask, requests)
├── .gitignore                          ← Est1 (Paso 3) - excluye venv/, __pycache__/
├── services/
│   ├── __init__.py                     ← Est1 (Paso 3)
│   └── api_service.py                  ← Est1 (Paso 4, 10) - CRUD generico + ejecutar_sp
├── routes/
│   ├── __init__.py                     ← Est1 (Paso 3)
│   ├── home.py                         ← Est1 (Paso 5) - Blueprint pagina inicio
│   ├── producto.py                     ← Est1 (Paso 6) - Blueprint CRUD Producto
│   ├── persona.py                      ← Est2 (Paso 7) - Blueprint CRUD Persona
│   ├── usuario.py                      ← Est3 (Paso 7) - Blueprint CRUD Usuario
│   ├── empresa.py                      ← Est1 (Paso 8) - Blueprint CRUD Empresa
│   ├── cliente.py                      ← Est2 (Paso 8) - Blueprint CRUD Cliente (FKs)
│   ├── rol.py                          ← Est3 (Paso 8) - Blueprint CRUD Rol
│   ├── ruta.py                         ← Est1 (Paso 9) - Blueprint CRUD Ruta
│   ├── vendedor.py                     ← Est2 (Paso 9) - Blueprint CRUD Vendedor (FK)
│   └── factura.py                      ← Est2 (Paso 10) - Blueprint Factura (SPs)
├── templates/
│   ├── layout/
│   │   └── base.html                   ← Est1 (Paso 5) - template base con sidebar
│   ├── components/
│   │   └── nav_menu.html               ← Est1 (Paso 5) + Est3 (Paso 9) - menu lateral
│   └── pages/
│       ├── home.html                   ← Est1 (Paso 5) + Est3 (Paso 10) - pagina inicio
│       ├── producto.html               ← Est1 (Paso 6) - CRUD Producto
│       ├── persona.html                ← Est2 (Paso 7) - CRUD Persona
│       ├── usuario.html                ← Est3 (Paso 7) - CRUD Usuario
│       ├── empresa.html                ← Est1 (Paso 8) - CRUD Empresa
│       ├── cliente.html                ← Est2 (Paso 8) - CRUD Cliente
│       ├── rol.html                    ← Est3 (Paso 8) - CRUD Rol
│       ├── ruta.html                   ← Est1 (Paso 9) - CRUD Ruta
│       ├── vendedor.html               ← Est2 (Paso 9) - CRUD Vendedor
│       └── factura.html                ← Est2 (Paso 10) - Factura maestro-detalle
├── static/
│   └── css/
│       └── app.css                     ← Est1 (Paso 5) - estilos del sidebar y responsive
├── scripts_bds/                        ← scripts SQL de la base de datos
└── venv/                               ← entorno virtual (NO se sube a GitHub)
```

### Paginas y sus URLs

| Pagina | URL | Tabla | Tipo | Responsable |
|--------|-----|-------|------|-------------|
| Home | `/` | - | Diagnostico | Est1 + Est3 |
| Producto | `/producto` | producto | CRUD simple | Est1 |
| Persona | `/persona` | persona | CRUD simple | Est2 |
| Usuario | `/usuario` | usuario | CRUD simple | Est3 |
| Empresa | `/empresa` | empresa | CRUD simple (2 campos) | Est1 |
| Cliente | `/cliente` | cliente | CRUD con FKs | Est2 |
| Rol | `/rol` | rol | CRUD con id int | Est3 |
| Ruta | `/ruta` | ruta | CRUD simple | Est1 |
| Vendedor | `/vendedor` | vendedor | CRUD con FK | Est2 |
| Factura | `/factura` | - (usa SPs) | Maestro-detalle | Est2 |

### Resumen de carga por estudiante

| Estudiante | Archivos creados | Archivos modificados | PRs |
|------------|-----------------|---------------------|-----|
| **Est1** | api_service.py, home.py, producto.py, empresa.py, ruta.py, base.html, nav_menu.html, home.html, producto.html, empresa.html, ruta.html, app.css | app.py | 7 |
| **Est2** | persona.py, cliente.py, vendedor.py, factura.py, persona.html, cliente.html, vendedor.html, factura.html | app.py | 4 |
| **Est3** | usuario.py, rol.py, usuario.html, rol.html | app.py, nav_menu.html, home.html | 4 |

---

## Comandos Git de Referencia Rapida

```powershell
# --- Comandos que se usan SIEMPRE antes de empezar una tarea nueva ---
git checkout main                          # volver a la rama principal
git pull                                   # descargar ultimos cambios
git checkout -b nombre-rama                # crear rama nueva para la tarea

# --- Comandos que se usan AL TERMINAR una tarea ---
git add .                                  # agregar todos los cambios
git commit -m "descripcion del cambio"     # crear commit con mensaje descriptivo
git push -u origin nombre-rama             # subir rama a GitHub
# Luego: crear PR en GitHub, pedir revision, merge

# --- Comandos para traer cambios de main a una rama existente ---
git fetch origin                           # descargar cambios de GitHub sin aplicarlos
git merge origin/main                      # aplicar cambios de main a la rama actual

# --- Comandos de consulta ---
git status                                 # ver estado actual (archivos modificados, rama)
git log --oneline -10                      # ver ultimos 10 commits
git branch                                 # ver ramas locales
git branch -a                              # ver todas las ramas (locales y remotas)
git diff                                   # ver cambios no agregados al staging
```

---

## Comparacion Flask vs Blazor

| Concepto | Flask (Python) | Blazor (C#) |
|----------|---------------|-------------|
| Archivo de pagina | `routes/producto.py` + `templates/pages/producto.html` | `Components/Pages/Producto.razor` |
| Servicio API | `services/api_service.py` | `Services/ApiService.cs` |
| Layout | `templates/layout/base.html` | `Components/Layout/MainLayout.razor` |
| Menu | `templates/components/nav_menu.html` | `Components/Layout/NavMenu.razor` |
| Registro de rutas | `app.register_blueprint(bp)` en `app.py` | `@page "/producto"` en cada `.razor` |
| Configuracion | `config.py` | `appsettings.json` + `Program.cs` |
| Inyeccion de servicio | `from services.api_service import ApiService` | `@inject ApiService Api` |
| Ejecutar | `python app.py` | `dotnet run` |
| Dependencias | `pip install -r requirements.txt` | NuGet + `.csproj` |
| Entorno virtual | `python -m venv venv` (obligatorio) | No necesita |

---

> Este archivo es el resumen completo del tutorial. Cada estudiante puede usarlo para repasar lo que hizo, verificar que no falta nada, o como guia para proyectos futuros.
