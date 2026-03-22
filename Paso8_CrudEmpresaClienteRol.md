# Paso 8 — CRUD Empresa (Est1), CRUD Cliente (Est2) y CRUD Rol (Est3)

Los tres estudiantes trabajan **en paralelo**, cada uno en su propia rama.

| Estudiante | Tabla | Rama | Campos | Nota |
|------------|-------|------|--------|------|
| **Estudiante 1** | empresa | `crud-empresa` | codigo, nombre | Tabla simple, 2 campos |
| **Estudiante 2** | cliente | `crud-cliente` | id (auto), credito, fkcodpersona, fkcodempresa | Tiene llaves foráneas (selects) |
| **Estudiante 3** | rol | `crud-rol` | id (int), nombre | La clave es `id` (int), no `codigo` (string) |

### ¿En qué orden se hacen los PRs?

Los PRs se pueden hacer **en cualquier orden** cuando cada uno toca archivos diferentes. Pero **Cliente depende de Empresa y Persona**: el formulario carga datos de esas tablas con `api.listar('persona')` y `api.listar('empresa')`. Conviene hacer merge de Empresa primero.

---

## Antes de empezar

Cada estudiante actualiza main y crea su rama:

```powershell
git checkout main          # volver a main
git pull                   # descargar últimos cambios
git checkout -b crud-empresa   # est1
git checkout -b crud-cliente   # est2
git checkout -b crud-rol       # est3
```

---

## Estudiante 1 — CRUD Empresa

Empresa es la tabla más simple: solo `codigo` y `nombre`.

### Archivos a crear

- `routes/empresa.py` — Blueprint con las 4 rutas CRUD
- `templates/pages/empresa.html` — Template con tabla y formulario
- Registrar Blueprint en `app.py`

### Subir cambios y crear PR

```powershell
git add .                                              # agrega archivos
git commit -m "Agregar ruta y template CRUD Empresa"   # guarda cambios
git push -u origin crud-empresa                        # sube la rama
```

---

## Estudiante 3 — CRUD Rol

Rol tiene una diferencia: la clave primaria es `id` (int), no `codigo` (string). El input usa `type="number"`.

### Archivos a crear

- `routes/rol.py` — Blueprint (CLAVE = 'id')
- `templates/pages/rol.html` — Template con campos id y nombre
- Registrar Blueprint en `app.py`

### Subir cambios y crear PR

```powershell
git add .                                          # agrega archivos
git commit -m "Agregar ruta y template CRUD Rol"   # guarda cambios
git push -u origin crud-rol                        # sube la rama
```

---

## Estudiante 2 — CRUD Cliente (con llaves foráneas)

Cliente es **más complejo** porque tiene llaves foráneas: cada cliente está asociado a una `persona` y opcionalmente a una `empresa`.

### Conceptos nuevos en Cliente

| Concepto | Explicación |
|----------|-------------|
| `api.listar('persona')` | Carga la lista de personas para llenar el select |
| `api.listar('empresa')` | Carga la lista de empresas para llenar el select |
| `<select name="fkcodpersona">` | Dropdown para elegir persona |
| `mapa_personas` | Diccionario codigo→nombre para mostrar nombres en la tabla |
| `or None` | Si empresa está vacío, envía null a la API |
| Campo `id` oculto | El id lo genera la BD, no se envía al crear |

### Archivos a crear

- `routes/cliente.py` — Blueprint con carga de personas y empresas
- `templates/pages/cliente.html` — Template con selects
- Registrar Blueprint en `app.py`

### Importante: orden de los PRs

El CRUD Cliente depende de que existan **persona** y **empresa** en el proyecto. Si Empresa aún no está mergeado, el estudiante 2 puede actualizar su rama después:

```powershell
git fetch origin            # descarga cambios de GitHub
git merge origin/main       # aplica cambios de main a la rama actual
```

### Subir cambios y crear PR

```powershell
git add .                                              # agrega archivos
git commit -m "Agregar ruta y template CRUD Cliente"   # guarda cambios
git push -u origin crud-cliente                        # sube la rama
```

---

## Después de los tres merges

**Los tres estudiantes** actualizan su main:

```powershell
git checkout main    # volver a main
git pull             # descargar cambios
```

---

> **Siguiente paso:** Paso 9 — CRUD Ruta, Vendedor y actualizar NavMenu.
