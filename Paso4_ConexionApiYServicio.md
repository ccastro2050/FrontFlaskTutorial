# Paso 4 — Conexión a la API y ApiService

**Quién lo hace:** Estudiante 1

**Rama:** `api-service`

Este paso crea el servicio que conecta el frontend Flask con la API REST. Es el equivalente a `Services/ApiService.cs` de Blazor.

---

## 1. ¿Qué es ApiService?

Es una clase Python que encapsula las 4 operaciones CRUD:

| Método | HTTP | URL | Qué hace |
|--------|------|-----|----------|
| `listar(tabla)` | GET | `/api/{tabla}` | Obtiene todos los registros |
| `crear(tabla, datos)` | POST | `/api/{tabla}` | Crea un registro nuevo |
| `actualizar(tabla, clave, valor, datos)` | PUT | `/api/{tabla}/{clave}/{valor}` | Modifica un registro |
| `eliminar(tabla, clave, valor)` | DELETE | `/api/{tabla}/{clave}/{valor}` | Borra un registro |

Cada Blueprint (ruta) importa esta clase y la usa para comunicarse con la API.

---

## 2. Crear el archivo `services/api_service.py`

```python
"""
api_service.py - Servicio generico que consume la API REST.

Contiene los 4 metodos CRUD (Listar, Crear, Actualizar, Eliminar)
que se reutilizan en todos los Blueprints/rutas.
"""

import requests
from config import API_BASE_URL


class ApiService:
    """Servicio generico para consumir la API REST."""

    def __init__(self):
        self.base_url = API_BASE_URL

    # ──────────────────────────────────────────────
    # LISTAR: GET /api/{tabla}
    # ──────────────────────────────────────────────
    def listar(self, tabla, limite=None):
        try:
            url = f"{self.base_url}/api/{tabla}"
            params = {}
            if limite:
                params['limite'] = limite

            respuesta = requests.get(url, params=params)
            datos_json = respuesta.json()
            return datos_json.get("datos", [])

        except requests.RequestException as ex:
            print(f"Error al listar {tabla}: {ex}")
            return []

    # ──────────────────────────────────────────────
    # CREAR: POST /api/{tabla}
    # ──────────────────────────────────────────────
    def crear(self, tabla, datos):
        try:
            url = f"{self.base_url}/api/{tabla}"
            respuesta = requests.post(url, json=datos)
            contenido = respuesta.json()
            mensaje = contenido.get("mensaje", "Operacion completada.")
            return (respuesta.ok, mensaje)

        except requests.RequestException as ex:
            return (False, f"Error de conexión: {ex}")

    # ──────────────────────────────────────────────
    # ACTUALIZAR: PUT /api/{tabla}/{clave}/{valor}
    # ──────────────────────────────────────────────
    def actualizar(self, tabla, nombre_clave, valor_clave, datos):
        try:
            url = f"{self.base_url}/api/{tabla}/{nombre_clave}/{valor_clave}"
            respuesta = requests.put(url, json=datos)
            contenido = respuesta.json()
            mensaje = contenido.get("mensaje", "Operacion completada.")
            return (respuesta.ok, mensaje)

        except requests.RequestException as ex:
            return (False, f"Error de conexión: {ex}")

    # ──────────────────────────────────────────────
    # ELIMINAR: DELETE /api/{tabla}/{clave}/{valor}
    # ──────────────────────────────────────────────
    def eliminar(self, tabla, nombre_clave, valor_clave):
        try:
            url = f"{self.base_url}/api/{tabla}/{nombre_clave}/{valor_clave}"
            respuesta = requests.delete(url)
            contenido = respuesta.json()
            mensaje = contenido.get("mensaje", "Operacion completada.")
            return (respuesta.ok, mensaje)

        except requests.RequestException as ex:
            return (False, f"Error de conexión: {ex}")
```

### ¿Qué hace cada parte?

| Código | Explicación |
|--------|-------------|
| `import requests` | Importa la librería para hacer peticiones HTTP |
| `from config import API_BASE_URL` | Trae la URL de la API desde `config.py` |
| `self.base_url = API_BASE_URL` | Guarda la URL como atributo para usarla en todos los métodos |
| `requests.get(url)` | Hace una petición GET (listar) |
| `requests.post(url, json=datos)` | Hace una petición POST con datos JSON (crear) |
| `requests.put(url, json=datos)` | Hace una petición PUT con datos JSON (actualizar) |
| `requests.delete(url)` | Hace una petición DELETE (eliminar) |
| `respuesta.json()` | Convierte la respuesta JSON a diccionario Python |
| `respuesta.ok` | `True` si el código HTTP es 200-299 (éxito) |
| `datos_json.get("datos", [])` | Extrae la lista de registros; si no existe, retorna lista vacía |
| `return (respuesta.ok, mensaje)` | Retorna una tupla: (éxito, mensaje) |

### Comparación con Blazor

| Flask (Python) | Blazor (C#) |
|----------------|-------------|
| `requests.get(url)` | `_http.GetFromJsonAsync(url)` |
| `requests.post(url, json=datos)` | `_http.PostAsJsonAsync(url, datos)` |
| `respuesta.json()` | Deserialización automática con `JsonElement` |
| `return (True, mensaje)` | `return (exito: true, mensaje: "...")` |
| `api = ApiService()` | `@inject ApiService Api` |

---

## 3. Verificar que compila

```powershell
python -c "from services.api_service import ApiService; print('ApiService OK')"   # verifica que importa sin errores
```

---

## 4. Subir cambios, PR y merge

```powershell
git add .                                    # agrega archivos al staging
git commit -m "Agregar ApiService y configurar conexión a la API"   # guarda cambios
git push -u origin api-service               # sube la rama a GitHub
```

En GitHub: crear Pull Request `api-service` → `main`, aprobar y hacer merge.
Después del merge, clic en **Delete branch**.

Después del merge, **Estudiante 2 y 3** actualizan:
```powershell
git checkout main    # volver a main
git pull             # descargar los cambios mergeados
```

---

> **Siguiente paso:** Paso 5 — Layout, Navegación y Página Home.
