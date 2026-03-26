# Paso 5 — Layout, Navegación y Página Home

**Quién lo hace:** Estudiante 1 (código compartido, se hace merge a main para que todos lo tengan).

**Rama:** `layout-navegacion-home`

---

## 1. Crear `static/css/app.css`

Este archivo contiene los estilos del sidebar, barra superior, iconos y responsive. Es idéntico al CSS que usa Blazor para su sidebar.

El archivo es largo (229 líneas de CSS) pero no hay que entenderlo línea por línea. Lo importante es:

| Sección | Qué hace |
|---------|----------|
| `.page` | Estructura flex: sidebar a la izquierda, contenido a la derecha |
| `.sidebar` | Fondo degradado azul-morado |
| `.navbar-toggler` | Botón hamburguesa para móvil (sin JavaScript) |
| `.nav-item .nav-link` | Estilo de los links del menú |
| `.nav-link.active` | Resalta el link de la página actual |
| `@media (min-width: 641px)` | En escritorio: sidebar fijo de 250px |
| `@media (max-width: 640px)` | En móvil: sidebar se oculta y aparece con hamburguesa |

---

## 2. Crear `templates/layout/base.html`

Este es el template base que envuelve todas las páginas. El equivalente a `MainLayout.razor` en Blazor.

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{% block title %}CRUD Facturas{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
          rel="stylesheet" />
    <link href="{{ url_for('static', filename='css/app.css') }}" rel="stylesheet" />
</head>
<body>
    <div class="page">
        <div class="sidebar">
            {% include 'components/nav_menu.html' %}
        </div>
        <main>
            <div class="top-row px-4">
                <span>Frontend Flask — API GenericaCsharp</span>
            </div>
            <article class="content px-4">
                {% with mensajes = get_flashed_messages(with_categories=true) %}
                    {% if mensajes %}
                        {% for categoria, mensaje in mensajes %}
                            <div class="alert alert-{{ categoria }} alert-dismissible fade show mt-3">
                                {{ mensaje }}
                                <button type="button" class="btn-close"
                                        onclick="this.parentElement.remove()"></button>
                            </div>
                        {% endfor %}
                    {% endif %}
                {% endwith %}
                {% block content %}{% endblock %}
            </article>
        </main>
    </div>
</body>
</html>
```

| Elemento | Función |
|----------|---------|
| `{% block title %}` | Cada página puede definir su propio título |
| `{{ url_for('static', ...) }}` | Genera la URL del archivo CSS |
| `{% include 'components/nav_menu.html' %}` | Inserta el menú lateral |
| `get_flashed_messages()` | Muestra alertas de éxito/error |
| `{% block content %}` | Aquí se inserta el contenido de cada página |

---

## 3. Crear `templates/components/nav_menu.html`

El menú lateral con links a las tablas. Por ahora solo incluye las tablas básicas (sin Cliente, Vendedor ni Factura).

```html
<div class="top-row ps-3 navbar navbar-dark">
    <div class="container-fluid">
        <a class="navbar-brand" href="/">CRUD Facturas</a>
    </div>
</div>

<input type="checkbox" title="Menu de navegacion" class="navbar-toggler" />

<div class="nav-scrollable">
    <nav class="nav flex-column">

        <div class="nav-item px-3">
            <a class="nav-link {{ 'active' if request.path == '/' }}" href="/">
                <span class="bi bi-house-door-fill-nav-menu"></span> Home
            </a>
        </div>

        <div class="nav-item px-3">
            <a class="nav-link {{ 'active' if request.path.startswith('/producto') }}" href="/producto">
                <span class="bi bi-list-nested-nav-menu"></span> Producto
            </a>
        </div>

        <div class="nav-item px-3">
            <a class="nav-link {{ 'active' if request.path.startswith('/persona') }}" href="/persona">
                <span class="bi bi-list-nested-nav-menu"></span> Persona
            </a>
        </div>

        <div class="nav-item px-3">
            <a class="nav-link {{ 'active' if request.path.startswith('/usuario') }}" href="/usuario">
                <span class="bi bi-list-nested-nav-menu"></span> Usuario
            </a>
        </div>

        <div class="nav-item px-3">
            <a class="nav-link {{ 'active' if request.path.startswith('/empresa') }}" href="/empresa">
                <span class="bi bi-list-nested-nav-menu"></span> Empresa
            </a>
        </div>

        <div class="nav-item px-3">
            <a class="nav-link {{ 'active' if request.path.startswith('/rol') }}" href="/rol">
                <span class="bi bi-list-nested-nav-menu"></span> Rol
            </a>
        </div>

        <div class="nav-item px-3">
            <a class="nav-link {{ 'active' if request.path.startswith('/ruta') }}" href="/ruta">
                <span class="bi bi-list-nested-nav-menu"></span> Ruta
            </a>
        </div>

    </nav>
</div>
```

La clase `active` se agrega automáticamente comparando `request.path` con la URL del link. En Blazor esto lo hace `NavLink` automáticamente.

---

## 4. Crear `templates/pages/home.html`

```html
{% extends 'layout/base.html' %}

{% block title %}CRUD Facturas{% endblock %}

{% block content %}
<div class="container mt-4">

    <h1>CRUD - Base de Datos Facturas</h1>

    <p class="lead">
        Frontend Flask que consume la API generica
        <strong>ApiGenericaCsharp</strong> para gestionar tablas
        de una base de datos.
    </p>

    <div class="alert alert-info">
        <strong>Tablas disponibles:</strong> Producto, Persona, Usuario, Empresa, Rol, Ruta.
        <br />
        Use el menú lateral para navegar a cada tabla.
    </div>

    {% if diagnostico and diagnostico.servidor %}
        <div class="card mt-4 border-secondary">
            <div class="card-header bg-secondary bg-opacity-10 text-muted py-2">
                <small><strong>Conexion activa</strong></small>
            </div>
            <div class="card-body py-2">
                <table class="table table-sm table-borderless mb-0" style="font-size: 0.85rem;">
                    <tbody>
                        {% if diagnostico.servidor.proveedor %}
                        <tr>
                            <td class="text-muted" style="width:160px">Proveedor</td>
                            <td><strong>{{ diagnostico.servidor.proveedor }}</strong></td>
                        </tr>
                        {% endif %}
                        {% if diagnostico.servidor.baseDatos %}
                        <tr>
                            <td class="text-muted">Base de datos</td>
                            <td><strong>{{ diagnostico.servidor.baseDatos }}</strong></td>
                        </tr>
                        {% endif %}
                        {% if diagnostico.servidor.version %}
                        <tr>
                            <td class="text-muted">Version</td>
                            <td><small>{{ diagnostico.servidor.version[:80] }}{% if diagnostico.servidor.version|length > 80 %}...{% endif %}</small></td>
                        </tr>
                        {% endif %}
                        {% if diagnostico.servidor.direccionIP %}
                        <tr>
                            <td class="text-muted">Servidor</td>
                            <td>{{ diagnostico.servidor.direccionIP }}{% if diagnostico.servidor.puerto %}:{{ diagnostico.servidor.puerto }}{% endif %}</td>
                        </tr>
                        {% endif %}
                        {% if diagnostico.servidor.usuarioConectado %}
                        <tr>
                            <td class="text-muted">Usuario</td>
                            <td>{{ diagnostico.servidor.usuarioConectado }}</td>
                        </tr>
                        {% endif %}
                    </tbody>
                </table>
            </div>
        </div>
    {% elif diagnostico is none %}
        <div class="mt-4">
            <small class="text-muted">No se pudo obtener informacion de conexión de la API.</small>
        </div>
    {% endif %}

</div>
{% endblock %}
```

---

## 5. Crear `routes/home.py`

```python
"""
home.py - Blueprint para la página de inicio.
"""

from flask import Blueprint, render_template
from services.api_service import ApiService
import requests

bp = Blueprint('home', __name__)
api = ApiService()


@bp.route('/')
def index():
    diagnostico = None
    try:
        url = f"{api.base_url}/api/diagnostico/conexión"
        respuesta = requests.get(url, timeout=3)
        if respuesta.ok:
            diagnostico = respuesta.json()
    except Exception:
        pass

    return render_template('pages/home.html', diagnostico=diagnostico)
```

---

## 6. Registrar el Blueprint en app.py

Modificar `app.py` para importar y registrar el Blueprint de Home:

**Antes:**
```python
# (Aqui se registraran los Blueprints en pasos posteriores)
```

**Después:**
```python
from routes.home import bp as home_bp
app.register_blueprint(home_bp)
```

---

## 7. Verificar que funciona

```powershell
python app.py   # debe arrancar en http://localhost:5300
```

Abrir `http://localhost:5300` en el navegador. Debe mostrar la página Home con el menú lateral.

---

## 8. Subir cambios, PR y merge

```powershell
git add .                                                              # agrega archivos
git commit -m "Configurar layout, navegacion y página Home"            # guarda cambios
git push -u origin layout-navegacion-home                              # sube la rama
```

Quien hizo push ve el botón amarillo "Compare & pull request" en GitHub y crea el PR: `layout-navegacion-home` → `main`. Si no aparece el botón: ir a la pestaña **Pull requests** → **New pull request**. Después, **Estudiante 1** va a la pestaña **Pull requests**, abre el PR, revisa en **Files changed**, y hace **Merge pull request** → **Confirm merge**.

Después del merge, **Estudiante 2 y Estudiante 3** actualizan:

```powershell
git checkout main    # volver a main
git pull             # descargar los cambios mergeados
```

---

> **Siguiente paso:** Paso 6 — CRUD Producto (Estudiante 1).
