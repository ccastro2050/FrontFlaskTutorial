# Paso 7 — CRUD Persona (Estudiante 2) y CRUD Usuario (Estudiante 3)

Los dos estudiantes trabajan **en paralelo**, cada uno en su propia rama.

| Estudiante | Tabla | Rama | Campos |
|------------|-------|------|--------|
| **Estudiante 2** | persona | `crud-persona` | codigo, nombre, email, telefono |
| **Estudiante 3** | usuario | `crud-usuario` | email (PK), contrasena |

Ambos siguen la misma estructura que Producto (Paso 6). Lo que cambia son los campos, el nombre de la tabla y el template.

**Importante:** cada estudiante debe registrar su Blueprint en `app.py`. Como ambos modifican el mismo archivo, el segundo PR podría tener un **conflicto de merge**. Ver la sección de resolución de conflictos al final.

---

## Antes de empezar

Cada estudiante actualiza main y crea su rama:

```powershell
git checkout main          # volver a main
git pull                   # descargar últimos cambios
git checkout -b crud-persona   # est2: crear rama
```

```powershell
git checkout main
git pull
git checkout -b crud-usuario   # est3: crear rama
```

---

## Estudiante 2 — CRUD Persona

Persona tiene 4 campos de texto: codigo (PK), nombre, email, telefono.

### 1. Crear `routes/persona.py`

```python
"""
persona.py - Blueprint CRUD para la tabla Persona.

Campos: codigo (PK), nombre, email, telefono
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.api_service import ApiService

bp = Blueprint('persona', __name__)
api = ApiService()
TABLA = 'persona'
CLAVE = 'codigo'


@bp.route('/persona')
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
            (r for r in registros if str(r.get(CLAVE)) == valor_clave), None
        )

    return render_template('pages/persona.html',
        registros=registros, mostrar_formulario=mostrar_formulario,
        editando=editando, registro=registro, limite=limite
    )


@bp.route('/persona/crear', methods=['POST'])
def crear():
    datos = {
        'codigo':   request.form.get('codigo', ''),
        'nombre':   request.form.get('nombre', ''),
        'email':    request.form.get('email', ''),
        'telefono': request.form.get('telefono', '')
    }
    exito, mensaje = api.crear(TABLA, datos)
    flash(mensaje, 'success' if exito else 'danger')
    return redirect(url_for('persona.index'))


@bp.route('/persona/actualizar', methods=['POST'])
def actualizar():
    valor = request.form.get('codigo', '')
    datos = {
        'nombre':   request.form.get('nombre', ''),
        'email':    request.form.get('email', ''),
        'telefono': request.form.get('telefono', '')
    }
    exito, mensaje = api.actualizar(TABLA, CLAVE, valor, datos)
    flash(mensaje, 'success' if exito else 'danger')
    return redirect(url_for('persona.index'))


@bp.route('/persona/eliminar', methods=['POST'])
def eliminar():
    valor = request.form.get('codigo', '')
    exito, mensaje = api.eliminar(TABLA, CLAVE, valor)
    flash(mensaje, 'success' if exito else 'danger')
    return redirect(url_for('persona.index'))
```

### 2. Crear `templates/pages/persona.html`

(Ver el código completo en el archivo creado por el tutor)

### 3. Registrar en app.py

Agregar estas líneas en `app.py`:

```python
from routes.persona import bp as persona_bp
app.register_blueprint(persona_bp)
```

### 4. Subir cambios y crear PR

```powershell
git add .                                          # agrega archivos
git commit -m "Agregar ruta y template CRUD Persona"   # guarda cambios
git push -u origin crud-persona                    # sube la rama
```

En GitHub: crear Pull Request `crud-persona` → `main`.
**Estudiante 1** revisa, aprueba y hace merge. Clic en **Delete branch**.

---

## Estudiante 3 — CRUD Usuario

Usuario tiene una diferencia: la clave primaria es `email` (no `codigo`) y el campo `contrasena` usa `type="password"`.

### 1. Crear `routes/usuario.py`

```python
"""
usuario.py - Blueprint CRUD para la tabla Usuario.

Campos: email (PK), contrasena
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.api_service import ApiService

bp = Blueprint('usuario', __name__)
api = ApiService()
TABLA = 'usuario'
CLAVE = 'email'


@bp.route('/usuario')
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
            (r for r in registros if str(r.get(CLAVE)) == valor_clave), None
        )

    return render_template('pages/usuario.html',
        registros=registros, mostrar_formulario=mostrar_formulario,
        editando=editando, registro=registro, limite=limite
    )


@bp.route('/usuario/crear', methods=['POST'])
def crear():
    datos = {
        'email':      request.form.get('email', ''),
        'contrasena': request.form.get('contrasena', '')
    }
    exito, mensaje = api.crear(TABLA, datos)
    flash(mensaje, 'success' if exito else 'danger')
    return redirect(url_for('usuario.index'))


@bp.route('/usuario/actualizar', methods=['POST'])
def actualizar():
    valor = request.form.get('email', '')
    datos = {
        'contrasena': request.form.get('contrasena', '')
    }
    exito, mensaje = api.actualizar(TABLA, CLAVE, valor, datos)
    flash(mensaje, 'success' if exito else 'danger')
    return redirect(url_for('usuario.index'))


@bp.route('/usuario/eliminar', methods=['POST'])
def eliminar():
    valor = request.form.get('email', '')
    exito, mensaje = api.eliminar(TABLA, CLAVE, valor)
    flash(mensaje, 'success' if exito else 'danger')
    return redirect(url_for('usuario.index'))
```

### 2. Crear `templates/pages/usuario.html`

(Ver el código completo en el archivo creado por el tutor)

### 3. Registrar en app.py

Agregar estas líneas en `app.py`:

```python
from routes.usuario import bp as usuario_bp
app.register_blueprint(usuario_bp)
```

### 4. Subir cambios y crear PR

```powershell
git add .                                           # agrega archivos
git commit -m "Agregar ruta y template CRUD Usuario"    # guarda cambios
git push -u origin crud-usuario                     # sube la rama
```

En GitHub: crear Pull Request `crud-usuario` → `main`.
**Estudiante 1** revisa, aprueba y hace merge. Clic en **Delete branch**.

---

## Conflicto en app.py (paso a paso)

Como ambos estudiantes modifican `app.py` (para registrar su Blueprint), el **segundo PR** muestra un conflicto. GitHub no puede hacer merge automáticamente porque ambos agregaron líneas en el mismo lugar.

### ¿Qué se ve en GitHub?

El PR muestra: **"This branch has conflicts that must be resolved"** con un botón **Resolve conflicts**.

### ¿Cómo resolverlo?

1. Clic en **Resolve conflicts** — se abre un editor con el archivo `app.py`

2. Se ven marcas de conflicto como estas:

```python
from routes.producto import bp as producto_bp
<<<<<<< crud-usuario (Current change)
from routes.usuario import bp as usuario_bp
app.register_blueprint(home_bp)
app.register_blueprint(producto_bp)
app.register_blueprint(usuario_bp)
=======
from routes.persona import bp as persona_bp
app.register_blueprint(home_bp)
app.register_blueprint(producto_bp)
app.register_blueprint(persona_bp)
>>>>>>> main (Incoming change)
```

3. **Borrar** las 3 líneas de marcas (`<<<<<<<`, `=======`, `>>>>>>>`)

4. **Borrar** las líneas duplicadas (los `register_blueprint` de home y producto aparecen dos veces)

5. El resultado debe quedar así:

```python
from routes.producto import bp as producto_bp
from routes.usuario import bp as usuario_bp
from routes.persona import bp as persona_bp
app.register_blueprint(home_bp)
app.register_blueprint(producto_bp)
app.register_blueprint(usuario_bp)
app.register_blueprint(persona_bp)
```

6. Clic en **Mark as resolved** (arriba a la derecha)

7. Clic en **Commit merge** (botón verde que aparece)

8. Ahora el PR puede mergearse: clic en **Merge pull request** → **Confirm merge**

### ¿Por qué pasó esto?

Porque ambos estudiantes agregaron una línea nueva en el mismo lugar de `app.py`. Git no sabe cuál va primero, así que pide que un humano lo decida. La solución es dejar **ambas** líneas (sin duplicados)

---

## "Subí el código equivocado en la rama de otro estudiante"

Esto pasa cuando un estudiante ejecuta los comandos git en la terminal equivocada. Por ejemplo, est2 ejecuta `git push -u origin crud-vendedor` pero en la carpeta de est3, subiendo el código de NavMenu en la branch de Vendedor.

**¿Qué pasa?** El código llega a GitHub y el PR se puede crear y mergear normalmente. El código final en `main` será correcto. Pero el PR dice "CRUD Vendedor" y tiene cambios de NavMenu — es confuso para quien revisa.

**¿Cómo solucionarlo?**

**Opción 1 (la más simple):** Cambiar el título del PR en GitHub para que coincida con lo que realmente tiene. Est1 (Scrum Master) revisa el contenido real del PR, no el título, y hace merge igual.

**Opción 2 (la correcta):** El estudiante corrige desde su terminal:

```powershell
git checkout main              # volver a main
git branch -D crud-vendedor    # borrar la rama local incorrecta
git checkout -b crud-vendedor  # crear la rama de nuevo desde main limpio
```

Luego vuelve a escribir su código, hace commit y push con `--force`:

```powershell
git add .
git commit -m "Agregar ruta y template CRUD Vendedor"
git push -u origin crud-vendedor --force   # sobreescribe la rama en GitHub
```

**¿Cuándo usar cada opción?**
- Si el PR aún no fue mergeado → Opción 2 (corregir)
- Si el PR ya fue mergeado → no importa, el código ya está en main

---

## Después de los dos merges

**Los tres estudiantes** actualizan su main:

```powershell
git checkout main    # volver a main
git pull             # descargar cambios
```

---

> **Siguiente paso:** Paso 8 — CRUD Empresa (Est1), CRUD Cliente (Est2) y CRUD Rol (Est3).
