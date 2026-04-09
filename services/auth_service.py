"""
auth_service.py - Servicio de autenticacion contra la API generica C#.

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
        # requests.Session() reutiliza la conexion HTTP (mas eficiente que crear una nueva cada vez)
        self.session = requests.Session()

    # ──────────────────────────────────────────────────────────
    # LOGIN: Verificar credenciales contra la API
    # ──────────────────────────────────────────────────────────
    def login(self, email, contrasena):
        """
        Autentica al usuario contra la API generica.

        La API tiene un endpoint especial para autenticacion:
          POST /api/autenticacion/token

        Le enviamos un JSON indicando:
          - tabla: en que tabla estan los usuarios (ej: "usuario")
          - campoUsuario: que columna es el login (ej: "email")
          - campoContrasena: que columna es la contrasena (ej: "contrasena")
          - usuario: el email ingresado
          - contrasena: la contrasena ingresada (texto plano)

        La API internamente:
          1. Busca el usuario en la tabla por email
          2. Compara la contrasena con BCrypt (hash irreversible)
          3. Si coincide, genera un token JWT y lo retorna

        Retorna:
          (True, {token: "...", ...})  si las credenciales son correctas
          (False, {mensaje: "..."})    si son incorrectas o hay error
        """
        try:
            resp = self.session.post(
                f"{self.base_url}/api/autenticacion/token",
                json={
                    "tabla": "usuario",
                    "campoUsuario": "email",
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

        Proceso:
          1. Trae TODOS los registros de la tabla "rol_usuario"
             (cada registro vincula un email con un id de rol)
          2. Trae TODOS los registros de la tabla "rol"
             (cada registro tiene id y nombre del rol)
          3. Filtra: busca en rol_usuario los que coincidan con el email
          4. Para cada match, busca el nombre del rol en la tabla "rol"

        Ejemplo con datos:
          rol_usuario: [{fkemail: "juan@mail.com", fkidrol: 2}, {fkemail: "juan@mail.com", fkidrol: 3}]
          rol: [{id: 1, nombre: "Admin"}, {id: 2, nombre: "Vendedor"}, {id: 3, nombre: "Bodeguero"}]

          Resultado para juan@mail.com: ["Vendedor", "Bodeguero"]
        """
        try:
            # Paso 1: Traer todas las asignaciones usuario-rol
            roles_usuario = self.session.get(
                f"{self.base_url}/api/rol_usuario", params={"limite": SIN_LIMITE}, timeout=30
            ).json().get("datos", [])

            # Paso 2: Traer todos los roles (para saber sus nombres)
            roles = self.session.get(
                f"{self.base_url}/api/rol", params={"limite": SIN_LIMITE}, timeout=30
            ).json().get("datos", [])

            # Paso 3: Crear un diccionario id -> nombre para busqueda rapida
            # Ejemplo: {"1": "Admin", "2": "Vendedor", "3": "Bodeguero"}
            rol_map = {str(r.get("id", "")): r.get("nombre", "") for r in roles}

            # Paso 4: Filtrar los roles que pertenecen a este usuario
            mis_roles = []
            for ru in roles_usuario:
                # Comparar email en minusculas para evitar problemas de mayusculas
                if (ru.get("email") or "").strip().lower() == email.strip().lower():
                    nombre_rol = rol_map.get(str(ru.get("fkidrol", "")), "")
                    if nombre_rol and nombre_rol not in mis_roles:
                        mis_roles.append(nombre_rol)
            return mis_roles
        except Exception:
            return []

    # ──────────────────────────────────────────────────────────
    # RUTAS PERMITIDAS: Obtener a que paginas puede acceder
    # ──────────────────────────────────────────────────────────
    def obtener_rutas_permitidas(self, roles):
        """
        Obtiene las rutas (paginas) permitidas segun los roles del usuario.

        Proceso:
          1. Trae TODOS los registros de "rutarol" (vincula rol con ruta)
          2. Trae TODOS los roles para obtener sus IDs
          3. Filtra: de los roles del usuario, obtiene sus IDs
          4. Busca en rutarol cuales rutas estan asignadas a esos IDs

        Ejemplo:
          El usuario tiene roles ["Vendedor"] -> id 2
          rutarol tiene: [{fkidrol: 2, fkruta: "/producto"}, {fkidrol: 2, fkruta: "/cliente"}]
          Resultado: {"/producto", "/cliente"}

        El middleware usara este set para permitir o bloquear el acceso.
        """
        try:
            # Todas las asignaciones rol-ruta
            rutas_rol = self.session.get(
                f"{self.base_url}/api/rutarol", params={"limite": SIN_LIMITE}, timeout=30
            ).json().get("datos", [])

            # Todos los roles (para convertir nombre -> id)
            roles_data = self.session.get(
                f"{self.base_url}/api/rol", params={"limite": SIN_LIMITE}, timeout=30
            ).json().get("datos", [])

            # Obtener los IDs de los roles que tiene el usuario
            # Ejemplo: roles=["Vendedor"] -> rol_ids={"2"}
            rol_ids = {str(r["id"]) for r in roles_data if r.get("nombre") in roles}

            # Filtrar rutas: solo las que pertenecen a los roles del usuario
            rutas = set()  # set() evita duplicados
            for rr in rutas_rol:
                if str(rr.get("fkidrol", "")) in rol_ids:
                    ruta = rr.get("fkruta", "")
                    if ruta:
                        rutas.add(ruta)
            return rutas
        except Exception:
            return set()

    # ──────────────────────────────────────────────────────────
    # DATOS DEL USUARIO: Obtener nombre, flags, etc.
    # ──────────────────────────────────────────────────────────
    def obtener_datos_usuario(self, email):
        """
        Obtiene todos los datos del usuario desde la tabla "usuario".

        Se usa para:
          - Mostrar el nombre del usuario en la interfaz
          - Verificar si debe_cambiar_contrasena es True (forzar cambio)

        Retorna un diccionario con todos los campos del usuario,
        o {} si no se encuentra.
        """
        try:
            usuarios = self.session.get(
                f"{self.base_url}/api/usuario", params={"limite": SIN_LIMITE}, timeout=30
            ).json().get("datos", [])
            for u in usuarios:
                if (u.get("email") or "").strip().lower() == email.strip().lower():
                    return u
        except Exception:
            pass
        return {}

    # ──────────────────────────────────────────────────────────
    # CAMBIAR CONTRASENA: Actualizar con encriptacion BCrypt
    # ──────────────────────────────────────────────────────────
    def actualizar_contrasena(self, email, nueva_contrasena):
        """
        Actualiza la contrasena del usuario en la BD.

        IMPORTANTE: El parametro ?encriptar=contrasena en la URL le dice a la API
        generica que debe encriptar el campo "contrasena" con BCrypt antes de guardarlo.
        Sin este parametro, la contrasena se guardaria en texto plano (inseguro).

        La API internamente:
          1. Recibe la contrasena en texto plano
          2. Genera un hash BCrypt (con salt aleatorio, cost factor 12)
          3. Guarda el hash en la BD (el texto plano nunca se almacena)

        El hash BCrypt es irreversible: no se puede obtener la contrasena original
        a partir del hash. Solo se puede verificar si una contrasena coincide.
        Ejemplo de hash: "$2a$12$LJ3m4ys1ZxB5R..." (60 caracteres)
        """
        try:
            # PUT /api/usuario/email/{email}?encriptar=contrasena
            url = f"{self.base_url}/api/usuario/email/{email}?encriptar=contrasena"
            resp = self.session.put(url, json={"contrasena": nueva_contrasena}, timeout=30)
            if resp.ok:
                return True, "Contrasena actualizada."
            msg = resp.json().get("mensaje", "Error al actualizar.") if resp.text else "Error al actualizar."
            return False, msg
        except Exception as e:
            return False, str(e)
