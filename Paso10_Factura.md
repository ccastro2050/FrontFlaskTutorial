# Paso 10 — Factura con Stored Procedures (Maestro-Detalle)

Factura es la página más compleja del proyecto. Usa **Stored Procedures (SPs)** porque una factura es una operación **maestro-detalle**: una factura tiene muchos productos.

Este paso se divide en **3 tareas con dependencias**:

| Orden | Estudiante | Tarea | Rama | Depende de |
|-------|------------|-------|------|------------|
| 1ro | **Estudiante 1** | Agregar método `ejecutar_sp` a ApiService | `agregar-ejecutar-sp` | Nada |
| 2do | **Estudiante 3** | Actualizar Home con todas las tablas | `actualizar-home` | Nada |
| 3ro | **Estudiante 2** | Crear `routes/factura.py` + `templates/pages/factura.html` | `crud-factura` | ejecutar_sp (Est1) |

**Importante:** Estudiante 2 debe esperar a que el PR de Estudiante 1 esté mergeado antes de subir su PR.

---

## Estudiante 1 — Agregar `ejecutar_sp` a ApiService

Agregar un nuevo método a `services/api_service.py` para ejecutar Stored Procedures.

### Agregar al final de la clase ApiService en `services/api_service.py`:

```python
    # ──────────────────────────────────────────────
    # EJECUTAR SP: POST /api/procedimientos/ejecutarsp
    # ──────────────────────────────────────────────
    def ejecutar_sp(self, nombre_sp, parametros=None):
        try:
            import json as json_mod
            url = f"{self.base_url}/api/procedimientos/ejecutarsp"

            payload = {"nombreSP": nombre_sp}
            if parametros:
                payload.update(parametros)

            respuesta = requests.post(url, json=payload)
            contenido = respuesta.json()

            if not respuesta.ok:
                mensaje = contenido.get("mensaje", "Error al ejecutar el procedimiento.")
                return (False, mensaje)

            resultados = contenido.get("resultados", [])
            if resultados:
                p_resultado = resultados[0].get("p_resultado") or resultados[0].get("@p_resultado")
                if p_resultado is not None:
                    if isinstance(p_resultado, str):
                        return (True, json_mod.loads(p_resultado))
                    return (True, p_resultado)

            return (True, contenido)

        except requests.RequestException as ex:
            return (False, f"Error de conexión: {ex}")
        except Exception as ex:
            return (False, f"Error procesando respuesta: {ex}")
```

### Subir cambios y crear PR

```powershell
git add .                                                      # agrega archivos
git commit -m "Agregar metodo ejecutar_sp a ApiService"        # guarda cambios
git push -u origin agregar-ejecutar-sp                         # sube la rama
```

Quien hizo push crea el PR en GitHub (botón amarillo "Compare & pull request"). **Estudiante 1** revisa, hace **Merge pull request** → **Confirm merge** → **Delete branch**.

---

## Estudiante 3 — Actualizar Home

Modificar `templates/pages/home.html`, cambiar la línea de tablas disponibles:

**Antes:**
```html
<strong>Tablas disponibles:</strong> Producto, Persona, Usuario, Empresa, Rol, Ruta.
```

**Después:**
```html
<strong>Tablas disponibles:</strong> Producto, Persona, Usuario, Empresa, Rol, Ruta, Cliente, Vendedor, Factura.
```

### Subir cambios y crear PR

```powershell
git add .                                                          # agrega archivos
git commit -m "Actualizar Home con lista completa de tablas"       # guarda cambios
git push -u origin actualizar-home                                 # sube la rama
```

Quien hizo push crea el PR en GitHub (botón amarillo "Compare & pull request"). **Estudiante 1** revisa, hace **Merge pull request** → **Confirm merge** → **Delete branch**.

---

## Estudiante 2 — Crear Factura

**Requisito:** el PR de Estudiante 1 (ejecutar_sp) debe estar mergeado. Actualizar la rama:

```powershell
git fetch origin            # descarga cambios de GitHub
git merge origin/main       # aplica cambios de main a la rama actual
```

### Archivos a crear

- `routes/factura.py` — Blueprint con 6 rutas (listar, ver, nueva, crear, editar, actualizar, eliminar)
- `templates/pages/factura.html` — Template con 3 vistas (listar, ver, formulario) + JavaScript para productos dinámicos
- Registrar en `app.py`:
  ```python
  from routes.factura import bp as factura_bp
  app.register_blueprint(factura_bp)
  ```

### Subir cambios y crear PR

```powershell
git add .                                                      # agrega archivos
git commit -m "Agregar página Factura con stored procedures"   # guarda cambios
git push -u origin crud-factura                                # sube la rama
```

Quien hizo push crea el PR en GitHub (botón amarillo "Compare & pull request"). **Estudiante 1** revisa, hace **Merge pull request** → **Confirm merge** → **Delete branch**.

---

## Después de los tres merges

**Los tres estudiantes** actualizan:

```powershell
git checkout main    # volver a main
git pull             # descargar cambios
```

El proyecto está completo con 9 páginas CRUD + Factura.

---

## Resumen final del proyecto

| Paso | Quién | Qué |
|------|-------|-----|
| 0 | Todos | Plan de desarrollo y buenas prácticas |
| 1-2 | Todos | Conceptos Flask y Herramientas |
| 3 | Est1 crea repo, Est2 y Est3 clonan | Proyecto + GitHub |
| 4 | Est1 | ApiService + conexión API |
| 5 | Est1 | Layout, navegación, Home |
| 6 | Est1 | CRUD Producto |
| 7 | Est2 + Est3 | CRUD Persona + CRUD Usuario |
| 8 | Est1 + Est2 + Est3 | CRUD Empresa + Cliente + Rol |
| 9 | Est1 + Est2 + Est3 | CRUD Ruta + Vendedor + NavMenu |
| 10 | Est1 + Est2 + Est3 | ejecutar_sp + Factura + Home |
