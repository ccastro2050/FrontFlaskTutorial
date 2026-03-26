# FrontFlaskTutorial

**Profesor:** Carlos Arturo Castro Castro

Frontend web construido con **Flask (Python)** que consume una API REST genérica en C# (`ApiGenericaCsharp`) para gestionar las tablas de una base de datos de facturación.

---

## 1. Descripción del proyecto

Sistema web tipo **MPA (Multi-Page Application)** que permite realizar operaciones CRUD (Crear, Leer, Actualizar, Eliminar) sobre 9 tablas de una base de datos, más una página de facturación con maestro-detalle usando Stored Procedures.

El frontend **no accede directamente a la base de datos**. Toda la comunicación pasa por una API REST intermedia, siguiendo el principio de **separación de responsabilidades**:

```
┌──────────────┐       HTTP        ┌────────────────────┐       SQL        ┌──────────────┐
│   Frontend   │  ←────────────→   │   API REST (C#)    │  ←────────────→  │  Base de     │
│   Flask      │  GET/POST/PUT/DEL │  ApiGenericaCsharp  │  Queries/SPs    │  Datos       │
│   Puerto 5300│                   │  Puerto 5035       │                  │  (la que use │
│              │                   │                    │                  │   la API)    │
└──────────────┘                   └────────────────────┘                  └──────────────┘
```

---

## 2. Arquitectura

### 2.1 Patrón arquitectónico: MVC adaptado

Flask no impone MVC estrictamente, pero este proyecto lo adapta así:

| Capa | Rol | Archivos |
|------|-----|----------|
| **Modelo (M)** | No hay modelos locales. Los datos vienen de la API como diccionarios JSON | La API los maneja |
| **Vista (V)** | Templates HTML con Jinja2 que renderizan los datos | `templates/pages/*.html` |
| **Controlador (C)** | Blueprints que reciben peticiones, llaman al servicio y pasan datos a la vista | `routes/*.py` |
| **Servicio** | Capa adicional que encapsula las llamadas HTTP a la API | `services/api_service.py` |

### 2.2 Flujo de una petición (ejemplo: listar productos)

```
1. El usuario abre http://localhost:5300/producto
         ↓
2. Flask busca la ruta "/" en el Blueprint "producto" (routes/producto.py)
         ↓
3. La función listar() se ejecuta:
   - Llama a api.listar("producto")
         ↓
4. ApiService hace GET http://localhost:5035/api/producto
         ↓
5. La API consulta la base de datos y retorna JSON:
   {"datos": [{"codigo": "P001", "nombre": "Laptop", ...}]}
         ↓
6. ApiService extrae la lista de datos y la retorna
         ↓
7. La función listar() pasa los datos al template:
   render_template("pages/producto.html", productos=datos)
         ↓
8. Jinja2 renderiza el HTML con los datos y lo envía al navegador
```

### 2.3 Flujo de una operación de escritura (ejemplo: crear producto)

```
1. El usuario llena el formulario y hace clic en "Guardar"
         ↓
2. El navegador envía POST /producto/crear con los datos del formulario
         ↓
3. Flask ejecuta la función crear() en routes/producto.py:
   - Lee los datos del formulario con request.form
   - Llama a api.crear("producto", datos)
         ↓
4. ApiService hace POST http://localhost:5035/api/producto con JSON
         ↓
5. La API inserta en la base de datos y retorna éxito/error
         ↓
6. La función crear() muestra un mensaje flash y redirige a la lista
```

---

## 3. Tecnologías y conceptos

### 3.1 Stack tecnológico

| Tecnología | Versión | Rol |
|-----------|---------|-----|
| **Python** | 3.x | Lenguaje de programación |
| **Flask** | 3.1.3 | Microframework web (servidor, rutas, templates) |
| **Jinja2** | 3.1.6 | Motor de templates (viene con Flask) |
| **requests** | 2.32.5 | Librería HTTP para consumir la API REST |
| **Bootstrap** | 5.3 | Framework CSS para diseño visual (vía CDN) |
| **Werkzeug** | 3.1.6 | Servidor WSGI que Flask usa internamente |
| **Git / GitHub** | - | Control de versiones y colaboración |

### 3.2 Conceptos clave de Flask

| Concepto | Qué es | Dónde se usa |
|----------|--------|-------------|
| **Blueprint** | Módulo que agrupa rutas relacionadas. Permite dividir la app en partes independientes | Cada tabla tiene su Blueprint en `routes/` |
| **Ruta (@bp.route)** | Decorador que asocia una URL con una función Python | Cada operación CRUD tiene su ruta |
| **Template (Jinja2)** | Archivo HTML con sintaxis especial (`{{ }}`, `{% %}`) para insertar datos dinámicos | `templates/pages/*.html` |
| **render_template** | Función que toma un template y datos, genera HTML y lo envía al navegador | En cada función de ruta |
| **request.form** | Diccionario con los datos enviados por un formulario HTML (método POST) | En las funciones crear/editar |
| **redirect / url_for** | Funciones para redirigir al usuario a otra página después de una operación | Después de crear/editar/eliminar |
| **flash** | Sistema de mensajes temporales (éxito, error) que se muestran una vez | Después de cada operación CRUD |
| **secret_key** | Clave para firmar las cookies de sesión (necesaria para flash y sesiones) | `config.py` |

### 3.3 Conceptos de la API REST

| Concepto | Qué es |
|----------|--------|
| **REST** | Estilo de arquitectura para APIs web. Usa HTTP (GET, POST, PUT, DELETE) para operar sobre recursos |
| **Endpoint** | URL específica de la API (ej: `GET /api/producto` lista productos) |
| **JSON** | Formato de intercambio de datos entre el frontend y la API |
| **CRUD** | Las 4 operaciones básicas: Create, Read, Update, Delete |
| **Stored Procedure (SP)** | Función almacenada en la base de datos que ejecuta lógica compleja (ej: crear factura con detalle) |

### 3.4 Mapeo HTTP → CRUD → API

| Operación | Método HTTP | Endpoint de la API | Método en ApiService |
|-----------|------------|-------------------|---------------------|
| Listar | GET | `/api/{tabla}` | `listar(tabla)` |
| Crear | POST | `/api/{tabla}` | `crear(tabla, datos)` |
| Actualizar | PUT | `/api/{tabla}/{clave}/{valor}` | `actualizar(tabla, clave, valor, datos)` |
| Eliminar | DELETE | `/api/{tabla}/{clave}/{valor}` | `eliminar(tabla, clave, valor)` |
| Ejecutar SP | POST | `/api/procedimientos/ejecutarsp` | `ejecutar_sp(nombre, params)` |

---

## 4. Estructura del proyecto

```
FrontFlaskTutorial/
├── app.py                           ← Punto de entrada: crea Flask, registra Blueprints
├── config.py                        ← Configuración: URL de la API, clave secreta
├── requirements.txt                 ← Dependencias (Flask, requests)
├── services/
│   ├── __init__.py
│   └── api_service.py               ← Servicio genérico: 5 métodos (CRUD + SP)
├── routes/
│   ├── __init__.py
│   ├── home.py                      ← Blueprint: página de inicio
│   ├── producto.py                  ← Blueprint: CRUD Producto
│   ├── persona.py                   ← Blueprint: CRUD Persona
│   ├── usuario.py                   ← Blueprint: CRUD Usuario
│   ├── empresa.py                   ← Blueprint: CRUD Empresa
│   ├── cliente.py                   ← Blueprint: CRUD Cliente (con FKs)
│   ├── rol.py                       ← Blueprint: CRUD Rol
│   ├── ruta.py                      ← Blueprint: CRUD Ruta
│   ├── vendedor.py                  ← Blueprint: CRUD Vendedor (con FK)
│   └── factura.py                   ← Blueprint: Factura maestro-detalle (SPs)
├── templates/
│   ├── layout/
│   │   └── base.html                ← Layout principal (Bootstrap + bloque content)
│   ├── components/
│   │   └── nav_menu.html            ← Menú lateral con links a todas las páginas
│   └── pages/
│       ├── home.html                ← Info de conexión a la BD
│       ├── producto.html            ← Tabla + formulario CRUD
│       ├── persona.html
│       ├── usuario.html
│       ├── empresa.html
│       ├── cliente.html             ← Con selects de FK (persona, empresa)
│       ├── rol.html
│       ├── ruta.html
│       ├── vendedor.html            ← Con select de FK (persona)
│       └── factura.html             ← Maestro-detalle con JavaScript
├── static/
│   └── css/                         ← Estilos CSS personalizados
└── venv/                            ← Entorno virtual Python (NO se sube a GitHub)
```

### Convención de archivos

Cada tabla de la base de datos tiene exactamente **2 archivos**:
- `routes/{tabla}.py` → Lógica Python (recibe peticiones, llama a la API, redirige)
- `templates/pages/{tabla}.html` → Vista HTML (muestra la tabla, el formulario, los botones)

Esto es diferente a Blazor (1 archivo .razor) y React (1 archivo .jsx), donde la lógica y la vista están juntas.

---

## 5. Patrones de diseño utilizados

| Patrón | Dónde se aplica | Qué resuelve |
|--------|----------------|-------------|
| **Service Layer** | `services/api_service.py` | Encapsula toda la comunicación HTTP en una clase reutilizable. Las rutas no hacen `requests.get()` directamente |
| **Blueprint (modular)** | `routes/*.py` | Divide la aplicación en módulos independientes. Cada Blueprint se puede desarrollar, probar y registrar por separado |
| **Template Inheritance** | `base.html` + `{% extends %}` | El layout se define una vez. Las páginas solo definen su contenido dentro de `{% block content %}` |
| **PRG (Post-Redirect-Get)** | Funciones crear/editar/eliminar | Después de un POST, redirige con `redirect()` para evitar que el usuario reenvíe el formulario al refrescar |
| **Flash Messages** | `flash()` + template | Mensajes de éxito/error que se muestran una vez y desaparecen al recargar |
| **Configuration Object** | `config.py` | Centraliza la configuración (URL de la API, clave secreta) en un solo archivo |

---

## 6. Páginas del sistema

| Página | Ruta | Tabla | Campos | Responsable |
|--------|------|-------|--------|-------------|
| Home | `/` | - | Info de conexión a la BD | Estudiante 1 |
| Producto | `/producto` | producto | codigo, nombre, stock, valorunitario | Estudiante 1 |
| Persona | `/persona` | persona | codigo, nombre, email, telefono | Estudiante 2 |
| Usuario | `/usuario` | usuario | codigo, nombre, email, clave | Estudiante 3 |
| Empresa | `/empresa` | empresa | codigo, nombre | Estudiante 1 |
| Cliente | `/cliente` | cliente | id (auto), credito, fkcodpersona, fkcodempresa | Estudiante 2 |
| Rol | `/rol` | rol | id, nombre | Estudiante 3 |
| Ruta | `/ruta` | ruta | ruta, descripcion | Estudiante 1 |
| Vendedor | `/vendedor` | vendedor | id (auto), carnet, direccion, fkcodpersona | Estudiante 2 |
| Factura | `/factura` | factura + factura_detalle | Maestro-detalle con SPs | Estudiante 2 |

---

## 7. Requisitos previos

- **Python 3.8+** instalado
- **API REST** (`ApiGenericaCsharp`) corriendo en `http://localhost:5035`
- **Base de datos** SQL Server, PostgreSQL, MySQL u otra con las tablas de facturación creadas
- **Git** instalado

---

## 8. Instalación y ejecución

```bash
# 1. Clonar el repositorio
git clone https://github.com/ccastro2050/FrontFlaskTutorial.git
cd FrontFlaskTutorial

# 2. Crear entorno virtual
python -m venv venv

# 3. Activar entorno virtual
# Windows (PowerShell):
venv\Scripts\Activate.ps1
# Windows (CMD):
venv\Scripts\activate.bat
# Linux/Mac:
source venv/bin/activate

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. Verificar que la API está corriendo
# (debe estar en http://localhost:5035)

# 6. Ejecutar
python app.py
```

Abrir en el navegador: **http://localhost:5300**

---

## 9. Flujo de trabajo con Git

```
Estudiante 2 o 3                              Estudiante 1
(en su PC)                                    (dueño del repo)
     |                                              |
  1. git checkout main                              |
  2. git pull                                       |
  3. git checkout -b feature/nombre                 |
  4. (escribe el código)                            |
  5. git add .                                      |
  6. git commit -m "feat: descripción"              |
  7. git push -u origin feature/nombre              |
     |                                              |
  8. Ve el botón amarillo en GitHub                 |
     "Compare & pull request"                       |
     Crea el Pull Request                           |
     |                                              |
     └──── le avisa a Estudiante 1 ────────────────→|
                                                    |
                                         9.  Va a la pestaña Pull requests
                                         10. Abre el PR, revisa en Files changed
                                         11. Merge pull request → Confirm merge
                                                    |
                                         Los cambios quedan en main
```

---

## 10. Comparación con otros frontends del mismo proyecto

| Aspecto | Flask (Python) | Blazor (C#) | React (JavaScript) |
|---------|---------------|-------------|-------------------|
| **Tipo de app** | MPA (recarga páginas) | SPA (SignalR) | SPA (cliente) |
| **Lenguaje** | Python | C# | JavaScript (JSX) |
| **Servidor dev** | `python app.py` | `dotnet run` | `npm run dev` |
| **Página CRUD** | 2 archivos: `.py` + `.html` | 1 archivo: `.razor` | 1 archivo: `.jsx` |
| **Servicio API** | `api_service.py` (requests) | `ApiService.cs` (HttpClient) | `ApiService.js` (fetch) |
| **Formularios** | `request.form` (POST) | `@bind` (two-way binding) | `useState` + `onChange` |
| **Navegación** | Links HTML (recarga completa) | NavLink (sin recarga) | React Router (sin recarga) |
| **Estado** | Sesiones del servidor | Variables en `@code` | `useState` / `useEffect` |
| **Puerto** | 5300 | 5235 | 5173 |

---

## 11. Distribución del trabajo

| Sprint | Paso | Estudiante 1 | Estudiante 2 | Estudiante 3 |
|--------|------|-------------|-------------|-------------|
| 1 | 1-3 | Crear repo + proyecto + GitHub | Clonar y verificar | Clonar y verificar |
| 2 | 4-5 | ApiService + Layout + Home | Pull y verificar | Pull y verificar |
| 3 | 6 | CRUD Producto | Pull y verificar | Pull y verificar |
| 4 | 7 | Revisar PRs + merge | CRUD Persona | CRUD Usuario |
| 5 | 8 | CRUD Empresa | CRUD Cliente | CRUD Rol |
| 6 | 9 | CRUD Ruta | CRUD Vendedor | NavMenu |
| 7 | 10 | Home actualizado | CRUD Factura | Revisar + verificar |

---

## 12. Tutorial paso a paso

El desarrollo completo está documentado en los archivos `Paso0` a `Paso11`:

| Archivo | Contenido |
|---------|----------|
| `Paso0_PlanDeDesarrollo.md` | Plan de desarrollo, buenas prácticas, historias de usuario |
| `Paso1_ConceptosBasicos.md` | Conceptos de Flask, Jinja2, Blueprint |
| `Paso2_Herramientas.md` | Instalación de Python, VS Code, Git |
| `Paso3_CrearProyectoYGitHub.md` | Crear proyecto Flask, GitHub, ramas |
| `Paso4_ConexionApiYServicio.md` | ApiService + config.py |
| `Paso5_LayoutNavegacionHome.md` | Layout, menú, página Home |
| `Paso6_CrudProducto.md` | Primer CRUD completo (modelo para los demás) |
| `Paso7_CrudPersonaYUsuario.md` | CRUD Persona (Est2) + CRUD Usuario (Est3) en paralelo |
| `Paso8_CrudEmpresaClienteRol.md` | CRUD Empresa (Est1) + CRUD Cliente (Est2) + CRUD Rol (Est3) |
| `Paso9_CrudRutaVendedorNavMenu.md` | CRUD Ruta (Est1) + CRUD Vendedor (Est2) + NavMenu (Est3) |
| `Paso10_Factura.md` | Factura maestro-detalle con Stored Procedures |
| `Paso11_ResumenFlujoCompleto.md` | Resumen final del proyecto |
