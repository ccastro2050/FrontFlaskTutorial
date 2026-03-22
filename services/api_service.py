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
            return (False, f"Error de conexion: {ex}")

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
            return (False, f"Error de conexion: {ex}")

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
            return (False, f"Error de conexion: {ex}")

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
            return (False, f"Error de conexion: {ex}")
        except Exception as ex:
            return (False, f"Error procesando respuesta: {ex}")
