# Paso 9 — CRUD Ruta (Est1), CRUD Vendedor (Est2) y Actualizar NavMenu (Est3)

Los tres estudiantes trabajan **en paralelo**, cada uno en su propia rama.

| Estudiante | Tarea | Rama | Nota |
|------------|-------|------|------|
| **Estudiante 1** | CRUD Ruta | `crud-ruta` | La clave primaria se llama `ruta` (igual que la tabla). Blueprint se llama `ruta_page` para evitar confusión |
| **Estudiante 2** | CRUD Vendedor | `crud-vendedor` | Tiene FK a persona + id autoincremental |
| **Estudiante 3** | Actualizar NavMenu | `actualizar-navmenu` | Agregar links de Cliente, Vendedor y Factura al menú |

### ¿En qué orden se hacen los merge?

Los merge se pueden hacer **en cualquier orden** porque cada uno toca archivos diferentes (ruta.py, vendedor.py, nav_menu.html). No hay dependencias entre ellos.

El único conflicto posible es en `app.py` (est1 y est2 agregan su Blueprint). Se resuelve igual que en el Paso 7: dejar ambas líneas sin duplicados.

---

## Antes de empezar

Cada estudiante actualiza main y crea su rama:

```powershell
git checkout main                  # volver a main
git pull                           # descargar últimos cambios
git checkout -b crud-ruta          # est1
git checkout -b crud-vendedor      # est2
git checkout -b actualizar-navmenu # est3
```

---

## Estudiante 1 — CRUD Ruta

Ruta tiene una particularidad: la clave primaria se llama `ruta`, igual que la tabla. Para evitar confusión en Flask, el Blueprint se llama `ruta_page`:

```python
bp = Blueprint('ruta_page', __name__)   # no 'ruta' para no confundir
```

Y en los templates se usa `url_for('ruta_page.index')` en vez de `url_for('ruta.index')`.

### Archivos a crear

- `routes/ruta.py` — Blueprint con CLAVE = 'ruta'
- `templates/pages/ruta.html` — Template con campos ruta y descripción
- Registrar en `app.py`:
  ```python
  from routes.ruta import bp as ruta_bp
  app.register_blueprint(ruta_bp)
  ```

### Verificar y subir

```powershell
git add .                                          # agrega archivos
git commit -m "Agregar ruta y template CRUD Ruta"  # guarda cambios
git push -u origin crud-ruta                       # sube la rama
```

Despues, **Estudiante 1** fusiona desde la terminal con `git fetch origin` + `git merge origin/nombre-rama` + `git push origin main`.

---

## Estudiante 2 — CRUD Vendedor

Vendedor es similar a Cliente: tiene FK a persona y id autoincremental.

### Archivos a crear

- `routes/vendedor.py` — Blueprint con select de persona
- `templates/pages/vendedor.html` — Template con select y mapa de nombres
- Registrar en `app.py`:
  ```python
  from routes.vendedor import bp as vendedor_bp
  app.register_blueprint(vendedor_bp)
  ```

### Verificar y subir

```powershell
git add .                                              # agrega archivos
git commit -m "Agregar ruta y template CRUD Vendedor"  # guarda cambios
git push -u origin crud-vendedor                       # sube la rama
```

Despues, **Estudiante 1** fusiona desde la terminal con `git fetch origin` + `git merge origin/nombre-rama` + `git push origin main`.

---

## Estudiante 3 — Actualizar NavMenu

Agregar links de **Cliente**, **Vendedor** y **Facturas** al menú lateral.

### Modificar `templates/components/nav_menu.html`

Agregar estos 3 bloques antes del cierre de `</nav>`:

```html
        <div class="nav-item px-3">
            <a class="nav-link {{ 'active' if request.path.startswith('/cliente') }}" href="/cliente">
                <span class="bi bi-list-nested-nav-menu"></span> Cliente
            </a>
        </div>

        <div class="nav-item px-3">
            <a class="nav-link {{ 'active' if request.path.startswith('/vendedor') }}" href="/vendedor">
                <span class="bi bi-list-nested-nav-menu"></span> Vendedor
            </a>
        </div>

        <div class="nav-item px-3">
            <a class="nav-link {{ 'active' if request.path.startswith('/factura') }}" href="/factura">
                <span class="bi bi-list-nested-nav-menu"></span> Facturas
            </a>
        </div>
```

### Verificar y subir

```powershell
git add .                                                              # agrega archivos
git commit -m "Agregar links de Cliente, Vendedor y Factura al menu"   # guarda cambios
git push -u origin actualizar-navmenu                                  # sube la rama
```

Despues, **Estudiante 1** fusiona desde la terminal con `git fetch origin` + `git merge origin/nombre-rama` + `git push origin main`.

---

## Después de los tres merges

**Los tres estudiantes** actualizan su main:

```powershell
git checkout main    # volver a main
git pull             # descargar cambios
```

Ahora el proyecto tiene 8 páginas CRUD y el menú completo.

---

> **Siguiente paso:** Paso 10 — Factura con Stored Procedures (maestro-detalle).
