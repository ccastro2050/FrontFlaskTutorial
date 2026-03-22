# Paso 1 — Conceptos Básicos de Flask

Este es el punto de partida. Aquí se cubren todos los conceptos que el proyecto utiliza, resumidos y con ejemplos directos.

---

## 1. ¿Qué es Flask?

Flask es un **microframework** de Python para construir aplicaciones web. Se llama "micro" porque viene con lo mínimo necesario y el desarrollador agrega lo que necesite.

```
Navegador  ←──HTTP──→  Flask (Python)  ←──HTTP──→  API REST (C#)
  (HTML)                (Rutas + Templates)          (Base de datos)
```

- El navegador hace peticiones HTTP al servidor Flask
- Flask procesa la petición, llama a la API si es necesario, y devuelve HTML
- A diferencia de Blazor (donde la lógica corre en el servidor con SignalR), Flask genera el HTML completo en cada petición

---

## 2. Comparación Flask vs Blazor

| Concepto | Blazor Server | Flask |
|----------|--------------|-------|
| Lenguaje | C# | Python |
| Tipo | Framework SPA (Single Page App) | Framework MPA (Multi Page App) |
| Comunicación | SignalR (WebSocket en tiempo real) | HTTP clásico (request/response) |
| Donde corre la lógica | Servidor, pero actualiza la página sin recargar | Servidor, y recarga la página completa |
| Archivos de página | `.razor` (HTML + C# juntos) | `.py` (lógica) + `.html` (vista separada) |
| Reactividad | Automática (cambiar variable actualiza la UI) | Manual (hay que renderizar el template de nuevo) |
| Curva de aprendizaje | Media (C# + Razor) | Baja (Python + HTML + Jinja2) |

---

## 3. Rutas (Routes)

En Flask, una **ruta** conecta una URL con una función de Python:

```python
from flask import Flask
app = Flask(__name__)

@app.route('/producto')
def listar_productos():
    return 'Lista de productos'
```

- `@app.route('/producto')` → cuando el usuario visita `/producto`, Flask ejecuta la función `listar_productos()`
- La función devuelve lo que el navegador mostrará

**En Blazor el equivalente es:** `@page "/producto"` al inicio de un archivo `.razor`

---

## 4. Blueprints

Cuando el proyecto crece, poner todas las rutas en `app.py` se vuelve un desorden. Los **Blueprints** permiten organizar las rutas en archivos separados:

```python
# routes/producto.py
from flask import Blueprint

bp = Blueprint('producto', __name__)

@bp.route('/producto')
def listar():
    return 'Lista de productos'
```

```python
# app.py
from routes.producto import bp as producto_bp
app.register_blueprint(producto_bp)
```

- Cada tabla tiene su propio archivo en `routes/`
- `Blueprint('producto', __name__)` crea un grupo de rutas con nombre "producto"
- `app.register_blueprint()` conecta esas rutas a la aplicación

**En Blazor el equivalente es:** cada archivo `.razor` es como un Blueprint separado

---

## 5. Templates (Jinja2)

Flask usa **Jinja2** para generar HTML dinámico. Los templates son archivos `.html` con marcas especiales:

```html
<!-- templates/pages/producto.html -->
<h1>Productos</h1>

{% for prod in productos %}
    <tr>
        <td>{{ prod.codigo }}</td>
        <td>{{ prod.nombre }}</td>
    </tr>
{% endfor %}
```

| Sintaxis Jinja2 | Qué hace | Equivalente Blazor |
|-----------------|----------|-------------------|
| `{{ variable }}` | Muestra el valor de una variable | `@variable` |
| `{% for item in lista %}` | Ciclo for | `@foreach (var item in lista)` |
| `{% if condicion %}` | Condicional | `@if (condicion)` |
| `{% extends "base.html" %}` | Hereda de otro template | Layout heredado automáticamente |
| `{% block content %}` | Define un bloque reemplazable | `@Body` en MainLayout |
| `{% include "nav.html" %}` | Incluye otro template | Componente embebido |

Para renderizar un template desde Python:

```python
from flask import render_template

@bp.route('/producto')
def listar():
    productos = [...]  # datos de la API
    return render_template('pages/producto.html', productos=productos)
```

`render_template()` toma el archivo HTML, reemplaza las variables y devuelve el HTML final.

---

## 6. Template base (Layout)

En Flask se usa **herencia de templates** para no repetir el HTML del menú y estructura en cada página:

```html
<!-- templates/layout/base.html -->
<!DOCTYPE html>
<html>
<head>
    <title>CRUD Facturas</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
</head>
<body>
    <div class="d-flex">
        {% include 'components/nav_menu.html' %}
        <main class="flex-grow-1 p-4">
            {% block content %}{% endblock %}
        </main>
    </div>
</body>
</html>
```

```html
<!-- templates/pages/producto.html -->
{% extends 'layout/base.html' %}

{% block content %}
    <h1>Productos</h1>
    <!-- contenido de la página -->
{% endblock %}
```

- `{% extends %}` dice "esta página usa la estructura de base.html"
- `{% block content %}` define dónde va el contenido de cada página
- `{% include %}` inserta otro template (como el menú)

**En Blazor el equivalente es:** `MainLayout.razor` con `@Body`

---

## 7. Formularios y métodos HTTP

En Flask, los formularios usan métodos HTTP:

```python
@bp.route('/producto/crear', methods=['GET', 'POST'])
def crear():
    if request.method == 'POST':
        # El usuario envió el formulario
        datos = {
            'codigo': request.form['codigo'],
            'nombre': request.form['nombre']
        }
        api.crear('producto', datos)
        return redirect('/producto')

    # El usuario abrió la página (GET)
    return render_template('pages/producto.html')
```

| Método | Cuándo se usa | Ejemplo |
|--------|--------------|---------|
| `GET` | El usuario abre la página | Visitar `/producto` |
| `POST` | El usuario envía un formulario | Clic en "Guardar" |

En el HTML:
```html
<form method="POST" action="/producto/crear">
    <input name="codigo" type="text">
    <input name="nombre" type="text">
    <button type="submit">Guardar</button>
</form>
```

**En Blazor:** no se usan formularios HTML clásicos. Se usa `@bind` y `@onclick` que envían datos por SignalR sin recargar la página.

---

## 8. Mensajes Flash

Flask tiene un sistema de **mensajes flash** para mostrar alertas (éxito, error) después de una acción:

```python
from flask import flash, redirect

@bp.route('/producto/crear', methods=['POST'])
def crear():
    resultado = api.crear('producto', datos)
    if resultado['exito']:
        flash('Producto creado exitosamente', 'success')
    else:
        flash(f'Error: {resultado["mensaje"]}', 'danger')
    return redirect('/producto')
```

En el template:
```html
{% with messages = get_flashed_messages(with_categories=true) %}
    {% for category, message in messages %}
        <div class="alert alert-{{ category }}">{{ message }}</div>
    {% endfor %}
{% endwith %}
```

- `flash('mensaje', 'categoria')` guarda un mensaje en la sesión
- `get_flashed_messages()` los recupera en el template (solo una vez)
- La categoría se usa como clase CSS de Bootstrap (`success` = verde, `danger` = rojo)

**En Blazor el equivalente es:** variables `mensaje` y `exito` que controlan un `<div class="alert">`.

---

## 9. Requests (peticiones HTTP a la API)

Flask usa la librería `requests` para llamar a la API REST:

```python
import requests

# GET - Listar productos
respuesta = requests.get('http://localhost:5035/api/producto')
datos = respuesta.json()

# POST - Crear producto
respuesta = requests.post('http://localhost:5035/api/producto', json=datos)

# PUT - Actualizar producto
respuesta = requests.put('http://localhost:5035/api/producto/codigo/P001', json=datos)

# DELETE - Eliminar producto
respuesta = requests.delete('http://localhost:5035/api/producto/codigo/P001')
```

| Método HTTP | Acción CRUD | requests |
|-------------|------------|----------|
| GET | Listar / Consultar | `requests.get(url)` |
| POST | Crear | `requests.post(url, json=datos)` |
| PUT | Actualizar | `requests.put(url, json=datos)` |
| DELETE | Eliminar | `requests.delete(url)` |

**En Blazor el equivalente es:** `HttpClient` con `GetFromJsonAsync`, `PostAsJsonAsync`, etc.

---

## 10. Entorno virtual (venv)

Python usa **entornos virtuales** para aislar las dependencias de cada proyecto:

```bash
python -m venv venv          # crear entorno virtual
venv\Scripts\activate        # activar (Windows)
pip install flask requests   # instalar dependencias
pip freeze > requirements.txt  # guardar lista de dependencias
```

- `venv/` es una carpeta con una copia de Python y las librerías instaladas
- **NO se sube a GitHub** (se agrega al `.gitignore`)
- Cada persona que clona el proyecto crea su propio `venv` e instala con `pip install -r requirements.txt`

**En Blazor el equivalente es:** las dependencias se manejan con NuGet y el archivo `.csproj`

---

> **Siguiente paso:** Paso 2 — Herramientas.
