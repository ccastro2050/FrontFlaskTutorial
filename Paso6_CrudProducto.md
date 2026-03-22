# Paso 6 — CRUD Producto

**Quién lo hace:** Estudiante 1

**Rama:** `crud-producto`

Este es el primer CRUD completo. Sirve como modelo para los demás. En Flask, cada CRUD tiene **dos archivos**: la ruta (Python) y el template (HTML).

---

## 1. ¿Cómo funciona un CRUD en Flask?

A diferencia de Blazor (donde todo está en un solo `.razor`), Flask separa la lógica del HTML:

```
routes/producto.py          ← Lógica (Python): recibe peticiones, llama a la API, redirige
templates/pages/producto.html  ← Vista (HTML): muestra la tabla, el formulario, los botones
```

El flujo es:

```
Usuario abre /producto
  → Flask ejecuta index() en producto.py
  → index() llama a api.listar("producto")
  → Pasa los datos a producto.html con render_template()
  → El navegador muestra la tabla

Usuario clic "Nuevo Producto"
  → El link lleva a /producto?accion=nuevo
  → index() ve accion='nuevo' y pasa mostrar_formulario=True
  → El template muestra el formulario vacío

Usuario llena campos y clic "Guardar"
  → El formulario hace POST a /producto/crear
  → crear() lee los campos con request.form
  → Llama a api.crear("producto", datos)
  → flash() guarda el mensaje de éxito/error
  → redirect() vuelve a /producto (la tabla se recarga)
```

---

## 2. Crear `routes/producto.py`

```python
"""
producto.py - Blueprint CRUD para la tabla Producto.

Campos: codigo (PK), nombre, stock (int), valorunitario (float)
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.api_service import ApiService

bp = Blueprint('producto', __name__)
api = ApiService()
TABLA = 'producto'
CLAVE = 'codigo'


@bp.route('/producto')
def index():
    limite = request.args.get('limite', type=int)
    accion = request.args.get('accion', '')
    valor_clave = request.args.get('clave', '')

    registros = api.listar(TABLA, limite)

    mostrar_formulario = accion in ('nuevo', 'editar')
    editando = accion == 'editar'

    registro = None
    if editando and valor_clave:
        registro = next(
            (r for r in registros if str(r.get(CLAVE)) == valor_clave),
            None
        )

    return render_template('pages/producto.html',
        registros=registros,
        mostrar_formulario=mostrar_formulario,
        editando=editando,
        registro=registro,
        limite=limite
    )


@bp.route('/producto/crear', methods=['POST'])
def crear():
    datos = {
        'codigo':        request.form.get('codigo', ''),
        'nombre':        request.form.get('nombre', ''),
        'stock':         request.form.get('stock', 0, type=int),
        'valorunitario': request.form.get('valorunitario', 0, type=float)
    }

    exito, mensaje = api.crear(TABLA, datos)
    flash(mensaje, 'success' if exito else 'danger')
    return redirect(url_for('producto.index'))


@bp.route('/producto/actualizar', methods=['POST'])
def actualizar():
    valor = request.form.get('codigo', '')
    datos = {
        'nombre':        request.form.get('nombre', ''),
        'stock':         request.form.get('stock', 0, type=int),
        'valorunitario': request.form.get('valorunitario', 0, type=float)
    }

    exito, mensaje = api.actualizar(TABLA, CLAVE, valor, datos)
    flash(mensaje, 'success' if exito else 'danger')
    return redirect(url_for('producto.index'))


@bp.route('/producto/eliminar', methods=['POST'])
def eliminar():
    valor = request.form.get('codigo', '')
    exito, mensaje = api.eliminar(TABLA, CLAVE, valor)
    flash(mensaje, 'success' if exito else 'danger')
    return redirect(url_for('producto.index'))
```

### ¿Qué hace cada parte?

| Código | Explicación |
|--------|-------------|
| `TABLA = 'producto'` | Nombre de la tabla en la API |
| `CLAVE = 'codigo'` | Nombre del campo clave primaria |
| `request.args.get('limite', type=int)` | Lee un parámetro de la URL (query string) |
| `request.form.get('codigo', '')` | Lee un campo del formulario HTML |
| `request.form.get('stock', 0, type=int)` | Lee un campo y lo convierte a entero |
| `flash(mensaje, 'success')` | Guarda un mensaje para mostrarlo como alerta |
| `redirect(url_for('producto.index'))` | Redirige al listado de productos |
| `next((r for r in registros if ...), None)` | Busca un registro por su clave en la lista |

---

## 3. Crear `templates/pages/producto.html`

```html
{% extends 'layout/base.html' %}

{% block title %}Productos{% endblock %}

{% block content %}
<div class="container mt-4">
    <h3>Productos</h3>

    {# ───────── BOTON NUEVO ───────── #}
    {% if not mostrar_formulario %}
        <a href="{{ url_for('producto.index', accion='nuevo') }}"
           class="btn btn-primary mb-3">
            Nuevo Producto
        </a>
    {% endif %}

    {# ───────── LIMITE DE REGISTROS ───────── #}
    <form method="GET" action="{{ url_for('producto.index') }}"
          class="d-flex align-items-center mb-3">
        <label class="form-label me-2 mb-0">Limite:</label>
        <input class="form-control me-2" type="number" name="limite"
               style="width:100px" value="{{ limite or '' }}" />
        <button class="btn btn-outline-secondary" type="submit">Cargar</button>
    </form>

    {# ───────── FORMULARIO (CREAR / EDITAR) ───────── #}
    {% if mostrar_formulario %}
        <div class="card mb-3">
            <div class="card-header">
                {{ "Editar Producto" if editando else "Nuevo Producto" }}
            </div>
            <div class="card-body">
                <form method="POST"
                      action="{{ url_for('producto.actualizar') if editando else url_for('producto.crear') }}"
                      onsubmit="{{ 'return confirm(\'¿Está seguro de actualizar el Producto?\')' if editando else '' }}">
                    <div class="row">
                        <div class="col-md-6 mb-3">
                            <label class="form-label">Codigo</label>
                            <input class="form-control" name="codigo"
                                   value="{{ registro.codigo if registro else '' }}"
                                   {{ 'readonly' if editando }} />
                        </div>
                        <div class="col-md-6 mb-3">
                            <label class="form-label">Nombre</label>
                            <input class="form-control" name="nombre"
                                   value="{{ registro.nombre if registro else '' }}" />
                        </div>
                        <div class="col-md-6 mb-3">
                            <label class="form-label">Stock</label>
                            <input class="form-control" type="number" name="stock"
                                   value="{{ registro.stock if registro else 0 }}" />
                        </div>
                        <div class="col-md-6 mb-3">
                            <label class="form-label">Valor Unitario</label>
                            <input class="form-control" type="number" step="0.01" name="valorunitario"
                                   value="{{ registro.valorunitario if registro else 0 }}" />
                        </div>
                    </div>
                    <button class="btn btn-success me-2" type="submit">Guardar</button>
                    <a href="{{ url_for('producto.index') }}" class="btn btn-secondary">Cancelar</a>
                </form>
            </div>
        </div>
    {% endif %}

    {# ───────── TABLA DE REGISTROS ───────── #}
    {% if registros %}
        <table class="table table-striped table-hover">
            <thead class="table-dark">
                <tr>
                    <th>Codigo</th>
                    <th>Nombre</th>
                    <th>Stock</th>
                    <th>Valor Unitario</th>
                    <th>Acciones</th>
                </tr>
            </thead>
            <tbody>
                {% for reg in registros %}
                <tr>
                    <td>{{ reg.codigo }}</td>
                    <td>{{ reg.nombre }}</td>
                    <td>{{ reg.stock }}</td>
                    <td>{{ reg.valorunitario }}</td>
                    <td>
                        <a href="{{ url_for('producto.index', accion='editar', clave=reg.codigo) }}"
                           class="btn btn-warning btn-sm me-1">Editar</a>

                        <form method="POST" action="{{ url_for('producto.eliminar') }}"
                              style="display:inline"
                              onsubmit="return confirm('¿Está seguro de eliminar el Producto \'{{ reg.codigo }}\'?')">
                            <input type="hidden" name="codigo" value="{{ reg.codigo }}" />
                            <button class="btn btn-danger btn-sm" type="submit">Eliminar</button>
                        </form>
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    {% else %}
        <div class="alert alert-warning">No se encontraron registros en la tabla producto.</div>
    {% endif %}

</div>
{% endblock %}
```

### Diferencias clave con Blazor

| Blazor | Flask |
|--------|-------|
| `@bind="campoCodigo"` (enlace bidireccional) | `name="codigo"` + `request.form.get('codigo')` |
| `@onclick="GuardarRegistro"` (sin recargar) | `<form method="POST">` (recarga la página) |
| `@if (mostrarFormulario)` | `{% if mostrar_formulario %}` |
| `@foreach (var reg in registros)` | `{% for reg in registros %}` |
| `confirm()` con `JS.InvokeAsync` | `onsubmit="return confirm(...)"` directo en HTML |
| Variables en `@code {}` | Variables pasadas desde Python con `render_template()` |

---

## 4. Registrar el Blueprint en app.py

Agregar en `app.py` después del registro de home:

```python
from routes.producto import bp as producto_bp
app.register_blueprint(producto_bp)
```

---

## 5. Verificar que funciona

```powershell
python app.py   # abrir http://localhost:5300/producto
```

---

## 6. Subir cambios, PR y merge

```powershell
git add .                                          # agrega archivos
git commit -m "Agregar pagina CRUD Producto"       # guarda cambios
git push -u origin crud-producto                   # sube la rama
```

En GitHub: crear Pull Request `crud-producto` → `main`, aprobar y hacer merge.

Después del merge, **Estudiante 2 y 3** actualizan:
```powershell
git checkout main    # volver a main
git pull             # descargar los cambios mergeados
```

---

> **Siguiente paso:** Paso 7 — CRUD Persona (Estudiante 2) y CRUD Usuario (Estudiante 3) en paralelo.
