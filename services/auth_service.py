"""Servicio de autenticacion y autorizacion contra la API.

QUE SE NECESITA PARA LOGIN Y CONTROL DE ACCESO:
=================================================

ARCHIVOS QUE SE CREAN (nuevos):
  services/auth_service.py              <- ESTE ARCHIVO: toda la logica de auth
  services/email_service.py             <- Envio de correos SMTP (contrasena temporal)
  routes/auth.py                        <- Rutas: /login, /logout, /cambiar, /recuperar
  middleware/auth_middleware.py          <- Intercepta cada request y verifica permisos
  templates/pages/login.html            <- Formulario de login
  templates/pages/cambiar_contrasena.html <- Formulario para cambiar contrasena
  templates/pages/recuperar_contrasena.html <- Recuperar contrasena por email SMTP
  templates/pages/sin_acceso.html       <- Pagina error 403 (no tiene permiso)

ARCHIVOS QUE SE MODIFICAN (existentes):
  config.py                             <- Agregar: variables SMTP (si no existen)
  app.py                                <- Agregar: crear_middleware(app) + auth_bp
  templates/layout/base.html            <- Agregar: boton login/logout en barra superior

TABLAS QUE SE NECESITAN EN LA BD (5):
  usuario      <- email (PK) + contrasena (BCrypt)
  rol          <- id + nombre (Administrador, Vendedor, etc)
  rol_usuario  <- vincula usuario con roles (N:M)
  ruta         <- id + ruta (/producto, /cliente, etc)
  rutarol      <- vincula roles con rutas (N:M)

LOS 3 CONCEPTOS CLAVE DE SEGURIDAD:
=====================================
1. AUTENTICACION = ¿Quien eres? (login, BCrypt, JWT)
2. AUTORIZACION = ¿Que puedes hacer? (roles, rutas, permisos)
3. ENCRIPTACION = ¿Como se protege? (BCrypt para contrasenas, SECRET_KEY para sesion, HTTPS)

COMO FUNCIONA LA AUTENTICACION:
===============================
1. El usuario envia email + contrasena desde el formulario de login.
2. Este servicio envia esos datos a la API generica C# (POST /api/autenticacion/token).
3. La API verifica la contrasena usando BCrypt (la contrasena se guarda encriptada en la BD).
4. Si es correcta, la API devuelve un token JWT.
5. Luego se consultan los ROLES del usuario (que puede hacer) y las RUTAS permitidas
   (a que paginas puede acceder).

TABLAS INVOLUCRADAS:
====================
- usuario:     contiene email, contrasena (hash BCrypt), nombre
- rol:         define roles del sistema (ej: "Administrador", "Vendedor")
- rol_usuario: vincula cada usuario con sus roles (tabla intermedia N:M)
- ruta:        cada pagina/endpoint del sistema (ej: "/producto", "/cliente")
- rutarol:     vincula cada rol con las rutas que puede acceder (tabla intermedia N:M)

DIAGRAMA DE RELACIONES:
=======================
  usuario ──< rol_usuario >── rol ──< rutarol >── ruta
  (email)    (fkemail,fkidrol)     (fkidrol,fkidruta)

  Ejemplo: El usuario "juan@mail.com" tiene rol "Vendedor" (id=2).
           El rol "Vendedor" tiene acceso a las rutas "/producto" y "/cliente".
           Entonces juan@mail.com puede acceder a /producto y /cliente.
"""

import requests
from config import API_BASE_URL

# Constante para traer todos los registros de una tabla (sin paginacion).
# La API generica usa ?limite=N para limitar resultados.
SIN_LIMITE = 999999


class AuthService:

    """
    Servicio que maneja toda la logica de autenticacion.
    Cada metodo hace llamadas HTTP a la API generica C#.
    """

    def __init__(self):
        # URL base de la API (ej: "http://localhost:5035")
        self.base_url = API_BASE_URL
        # requests.Session() reutiliza la conexion HTTP (mas eficiente)
        self.session = requests.Session()
        # Cache para guardar resultados de estructura (PKs, FKs).
        # Evita consultar la API multiples veces por la misma tabla.
        # Se llena la primera vez que se consulta y se reutiliza despues.
        self._fk_cache = {}

    # ──────────────────────────────────────────────────────────
    # METODOS INTERNOS: Descubrimiento dinamico de estructura
    # ──────────────────────────────────────────────────────────
    # Estos metodos consultan la API para saber como se llaman las
    # columnas PK y FK de cada tabla. Asi el servicio funciona con
    # cualquier base de datos sin hardcodear nombres de columnas.
    #
    # Ejemplo: en vez de asumir que rol_usuario tiene un campo "fkemail",
    # preguntamos a la API: "que columna de rol_usuario apunta a usuario?"
    # La API responde: "fkemail" (o como se llame en esa BD).
    #
    # Los resultados se guardan en _fk_cache para no repetir consultas.
    # ──────────────────────────────────────────────────────────

    def _obtener_estructura(self, tabla):
        """
        Obtiene la estructura de una tabla via GET /api/estructuras/{tabla}/modelo.
        Retorna una lista de columnas con sus propiedades:
          - column_name: nombre de la columna
          - data_type: tipo de dato (varchar, integer, etc)
          - is_primary_key: "YES" o "NO"
          - foreign_table_name: tabla a la que apunta (si es FK)
          - fk_constraint_name: nombre de la constraint FK
        """
        cache_key = f"estructura_{tabla}"
        if cache_key in self._fk_cache:
            return self._fk_cache[cache_key]
        try:
            resp = self.session.get(
                f"{self.base_url}/api/estructuras/{tabla}/modelo", timeout=30
            ).json()
            columnas = resp.get("datos", [])
            self._fk_cache[cache_key] = columnas
            return columnas
        except Exception:
            return []

    def _obtener_fk(self, tabla_origen, tabla_destino):
        """
        Descubre que columna de tabla_origen es FK hacia tabla_destino.

        Ejemplo: _obtener_fk("rol_usuario", "usuario") -> "fkemail"
                 _obtener_fk("rol_usuario", "rol") -> "fkidrol"
                 _obtener_fk("rutarol", "ruta") -> "fkidruta"

        Busca de dos formas (compatible con Postgres y SqlServer):
          1. Por foreign_table_name directo (Postgres lo devuelve correctamente)
          2. Por fk_constraint_name que contenga el nombre de la tabla destino
             (SqlServer a veces no devuelve foreign_table_name correctamente)
        """
        cache_key = f"{tabla_origen}->{tabla_destino}"
        if cache_key in self._fk_cache:
            return self._fk_cache[cache_key]
        columnas = self._obtener_estructura(tabla_origen)
        # 1. Buscar por foreign_table_name directo (Postgres)
        for col in columnas:
            if col.get("foreign_table_name") == tabla_destino:
                self._fk_cache[cache_key] = col["column_name"]
                return col["column_name"]
        # 2. Fallback: buscar en fk_constraint_name (SqlServer)
        for col in columnas:
            constraint = col.get("fk_constraint_name", "") or ""
            if tabla_destino in constraint.lower() and col.get("foreign_table_name"):
                self._fk_cache[cache_key] = col["column_name"]
                return col["column_name"]
        return None

    def _obtener_pk(self, tabla):
        """
        Descubre que columna es la PK de una tabla.

        Ejemplo: _obtener_pk("usuario") -> "email"
                 _obtener_pk("rol") -> "id"
                 _obtener_pk("ruta") -> "id"
        """
        cache_key = f"pk_{tabla}"
        if cache_key in self._fk_cache:
            return self._fk_cache[cache_key]
        columnas = self._obtener_estructura(tabla)
        for col in columnas:
            if col.get("is_primary_key") == "YES":
                self._fk_cache[cache_key] = col["column_name"]
                return col["column_name"]
        return "id"

    # ──────────────────────────────────────────────────────────
    # LOGIN: Verificar credenciales contra la API
    # ──────────────────────────────────────────────────────────
    def login(self, email, contrasena):
        """
        Autentica al usuario contra la API generica.
        La API verifica la contrasena con BCrypt (hash irreversible).
        Retorna (True, {token:...}) si OK, (False, {mensaje:...}) si falla.
        """
        try:
            pk_usuario = self._obtener_pk("usuario")
            resp = self.session.post(
                f"{self.base_url}/api/autenticacion/token",
                json={
                    "tabla": "usuario",
                    "campoUsuario": pk_usuario,
                    "campoContrasena": "contrasena",
                    "usuario": email,
                    "contrasena": contrasena
                }, timeout=30)
            if resp.ok:
                return True, resp.json()
            return False, resp.json() if resp.text else {"mensaje": "Error de autenticacion."}
        except Exception as e:
            return False, {"mensaje": str(e)}

    # ──────────────────────────────────────────────────────────
    # ROLES: Obtener que roles tiene el usuario
    # ──────────────────────────────────────────────────────────
    def obtener_roles_usuario(self, email):
        """
        Obtiene los nombres de roles asignados al usuario.
        Consulta rol_usuario (email->rol_id) y rol (id->nombre).
        """
        try:
            fk_email = self._obtener_fk("rol_usuario", "usuario")
            fk_rol = self._obtener_fk("rol_usuario", "rol")
            if not fk_email or not fk_rol:
                return []
            pk_rol = self._obtener_pk("rol")

            roles_usuario = self.session.get(
                f"{self.base_url}/api/rol_usuario", params={"limite": SIN_LIMITE}, timeout=30
            ).json().get("datos", [])
            roles = self.session.get(
                f"{self.base_url}/api/rol", params={"limite": SIN_LIMITE}, timeout=30
            ).json().get("datos", [])
            rol_map = {str(r.get(pk_rol, "")): r.get("nombre", "") for r in roles}
            mis_roles = []
            for ru in roles_usuario:
                ru_email = str(ru.get(fk_email, "")).strip().lower()
                if ru_email == email.strip().lower():
                    nombre_rol = rol_map.get(str(ru.get(fk_rol, "")), "")
                    if nombre_rol and nombre_rol not in mis_roles:
                        mis_roles.append(nombre_rol)
            return mis_roles
        except Exception:
            return []

    # ──────────────────────────────────────────────────────────
    # RUTAS PERMITIDAS: A que paginas puede acceder
    # ──────────────────────────────────────────────────────────
    def obtener_rutas_permitidas(self, roles):
        """
        Obtiene las rutas (paginas) permitidas segun los roles.
        El middleware usara este set para permitir o bloquear acceso.
        """
        try:
            fk_rol_en_rutarol = self._obtener_fk("rutarol", "rol")
            fk_ruta_en_rutarol = self._obtener_fk("rutarol", "ruta")
            if not fk_rol_en_rutarol:
                return set()
            pk_rol = self._obtener_pk("rol")
            pk_ruta = self._obtener_pk("ruta")

            rutas_rol = self.session.get(
                f"{self.base_url}/api/rutarol", params={"limite": SIN_LIMITE}, timeout=30
            ).json().get("datos", [])
            roles_data = self.session.get(
                f"{self.base_url}/api/rol", params={"limite": SIN_LIMITE}, timeout=30
            ).json().get("datos", [])
            rol_ids = {str(r[pk_rol]) for r in roles_data if r.get("nombre") in roles}

            # Obtener rutas completas para resolver el path
            rutas_data = self.session.get(
                f"{self.base_url}/api/ruta", params={"limite": SIN_LIMITE}, timeout=30
            ).json().get("datos", [])
            ruta_map = {str(r.get(pk_ruta, "")): r.get("ruta", "") for r in rutas_data}

            rutas = set()
            for rr in rutas_rol:
                if str(rr.get(fk_rol_en_rutarol, "")) in rol_ids:
                    # Intentar obtener la ruta del campo FK o de un campo "ruta" directo
                    ruta = ""
                    if fk_ruta_en_rutarol:
                        ruta_id = str(rr.get(fk_ruta_en_rutarol, ""))
                        ruta = ruta_map.get(ruta_id, "")
                    if not ruta:
                        ruta = rr.get("fkruta", "") or rr.get("ruta", "")
                    if ruta:
                        rutas.add(ruta)
            return rutas
        except Exception:
            return set()

    # ──────────────────────────────────────────────────────────
    # DATOS DEL USUARIO: nombre, flags, etc.
    # ──────────────────────────────────────────────────────────
    def obtener_datos_usuario(self, email):
        """Obtiene todos los datos del usuario desde la tabla."""
        try:
            pk_usuario = self._obtener_pk("usuario")
            usuarios = self.session.get(
                f"{self.base_url}/api/usuario", params={"limite": SIN_LIMITE}, timeout=30
            ).json().get("datos", [])
            for u in usuarios:
                if str(u.get(pk_usuario, "")).strip().lower() == email.strip().lower():
                    return u
        except Exception:
            pass
        return {}

    # ──────────────────────────────────────────────────────────
    # CAMBIAR CONTRASENA: con encriptacion BCrypt
    # ──────────────────────────────────────────────────────────
    def actualizar_contrasena(self, email, nueva_contrasena):
        """
        Actualiza la contrasena en la BD.
        El parametro ?camposEncriptar=contrasena le dice a la API que
        encripte con BCrypt antes de guardar. Sin esto, se guardaria
        en texto plano (inseguro).
        """
        try:
            pk_usuario = self._obtener_pk("usuario")
            url = f"{self.base_url}/api/usuario/{pk_usuario}/{email}?camposEncriptar=contrasena"
            resp = self.session.put(url, json={"contrasena": nueva_contrasena}, timeout=30)
            if resp.ok:
                return True, "Contrasena actualizada."
            msg = resp.json().get("mensaje", "Error al actualizar.") if resp.text else "Error al actualizar."
            return False, msg
        except Exception as e:
            return False, str(e)
