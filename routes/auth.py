"""
auth.py - Rutas (endpoints) de autenticacion.

Este archivo define las paginas web relacionadas con el login:
  /login                -> Formulario para iniciar sesion
  /logout               -> Cerrar sesion
  /cambiar-contrasena   -> Formulario para cambiar la contrasena
  /recuperar-contrasena -> Formulario para recuperar contrasena olvidada

CONCEPTOS CLAVE:
================
- Blueprint: Es una forma de organizar rutas en Flask. En vez de poner todas
  las rutas en app.py, las agrupamos por tema. Este blueprint agrupa las rutas
  de autenticacion. Se registra en app.py con app.register_blueprint(auth_bp).

- session: Es un diccionario que Flask guarda para cada usuario (en una cookie
  encriptada). Cuando el usuario hace login, guardamos sus datos aqui.
  Mientras la sesion exista, el usuario esta "logueado".

- flash(): Muestra mensajes temporales al usuario (alertas verdes, rojas, etc).
  Se muestran una sola vez y desaparecen al recargar la pagina.

- url_for(): Genera la URL de una ruta a partir de su nombre.
  Ejemplo: url_for("auth.login") -> "/login"
  Ejemplo: url_for("home.index") -> "/"

FLUJO COMPLETO DE LOGIN:
========================
  1. Usuario abre /login (GET) -> ve el formulario
  2. Escribe email y contrasena -> hace POST a /login
  3. Flask envia las credenciales a la API C# (AuthService.login)
  4. La API verifica con BCrypt -> retorna OK o error
  5. Si OK: se cargan roles y rutas permitidas en la sesion
  6. Se redirige al usuario a la pagina principal (/)
  7. El middleware (auth_middleware.py) verifica en cada request
     si el usuario puede acceder a esa ruta
"""

import random
import string
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from services.auth_service import AuthService
from services.email_service import enviar_contrasena_temporal

# Constante para consultas sin limite de registros
SIN_LIMITE = 999999

# Crear el Blueprint. El primer argumento "auth" es el nombre que se usa
# en url_for(). Ejemplo: url_for("auth.login") genera la URL "/login".
bp = Blueprint("auth", __name__)

# Instancia del servicio de autenticacion (hace las llamadas HTTP a la API)
auth = AuthService()

# Set en memoria para rastrear usuarios que deben cambiar contrasena.
# Cuando se recupera una contrasena, el email se agrega aqui.
# En el proximo login, se detecta y se fuerza el cambio.
# NOTA: Se pierde al reiniciar Flask (es en memoria, no en BD).
_emails_debe_cambiar = set()


# ══════════════════════════════════════════════════════════════
# VALIDACION DE CONTRASENA
# ══════════════════════════════════════════════════════════════
def validar_contrasena(pwd):
    """
    Valida que la contrasena cumpla requisitos minimos de seguridad.

    Reglas:
      - Minimo 6 caracteres
      - Al menos 1 letra mayuscula (A-Z)
      - Al menos 1 numero (0-9)
      - No puede ser trivial (123456, etc)

    Retorna:
      None si la contrasena es valida
      Un string con el mensaje de error si no es valida
    """
    if len(pwd) < 6:
        return "La contrasena debe tener al menos 6 caracteres."
    if not any(c.isupper() for c in pwd):
        return "Debe incluir al menos una letra mayuscula."
    if not any(c.isdigit() for c in pwd):
        return "Debe incluir al menos un numero."
    if pwd in ("123", "1234", "12345", "123456"):
        return "No puede usar una contrasena trivial."
    return None  # None = todo bien, la contrasena es valida


# ══════════════════════════════════════════════════════════════
# RUTA: /login (GET) - Mostrar formulario de login
# ══════════════════════════════════════════════════════════════
@bp.route("/login", methods=["GET"])
def login():
    """
    Muestra el formulario de login.
    Si el usuario ya tiene sesion activa, lo redirige al inicio.
    """
    # Si ya esta logueado, no tiene sentido mostrar el login de nuevo
    if session.get("usuario"):
        return redirect(url_for("home.index"))
    return render_template("pages/login.html")


# ══════════════════════════════════════════════════════════════
# RUTA: /login (POST) - Procesar el formulario de login
# ══════════════════════════════════════════════════════════════
@bp.route("/login", methods=["POST"])
def login_post():
    """
    Procesa el formulario de login. Este es el corazon de la autenticacion.

    Pasos:
      1. Leer email y contrasena del formulario
      2. Validar que no esten vacios
      3. Llamar a la API para autenticar (BCrypt verifica la contrasena)
      4. Si falla -> mostrar error
      5. Obtener roles del usuario (que puede hacer)
      6. Si no tiene roles -> no puede entrar
      7. Obtener rutas permitidas (a que paginas puede acceder)
      8. Obtener datos del usuario (nombre, etc)
      9. Guardar todo en la sesion de Flask
      10. Verificar si debe cambiar contrasena
      11. Redirigir al inicio
    """
    # Paso 1: Leer datos del formulario HTML
    # request.form es un diccionario con los datos del <form>
    email = request.form.get("email", "").strip()       # .strip() quita espacios
    contrasena = request.form.get("contrasena", "")

    # Paso 2: Validar que no esten vacios
    if not email or not contrasena:
        flash("Ingrese email y contrasena.", "danger")   # "danger" = alerta roja
        return render_template("pages/login.html")

    # Paso 3: Autenticar contra la API (la API verifica con BCrypt)
    exito, datos = auth.login(email, contrasena)
    if not exito:
        # Paso 4: Credenciales incorrectas
        flash(datos.get("mensaje", "Error de autenticacion."), "danger")
        return render_template("pages/login.html")

    # Paso 5: Obtener roles del usuario
    roles = auth.obtener_roles_usuario(email)
    if not roles:
        # Paso 6: Usuario sin roles no puede acceder
        flash("El usuario no tiene roles asignados.", "warning")  # "warning" = alerta amarilla
        return render_template("pages/login.html")

    # Paso 7 y 8: Obtener rutas permitidas y datos del usuario
    rutas_permitidas = auth.obtener_rutas_permitidas(roles)
    datos_usuario = auth.obtener_datos_usuario(email)

    # Paso 9: Guardar en la sesion de Flask
    # La sesion es una cookie encriptada que viaja con cada request.
    # Mientras estos datos existan en la sesion, el usuario esta "logueado".
    session["usuario"] = email                                    # Email del usuario
    session["nombre_usuario"] = datos_usuario.get("nombre", email)  # Nombre para mostrar
    session["token"] = datos.get("token", "")                     # Token JWT (para futuro uso)
    session["roles"] = roles                                      # Lista de roles: ["Admin", "Vendedor"]
    session["rutas_permitidas"] = list(rutas_permitidas)          # Lista de rutas: ["/producto", "/cliente"]

    # Paso 10: Verificar si debe cambiar contrasena
    # Esto pasa cuando: (a) el campo debe_cambiar_contrasena es True en la BD,
    # o (b) el usuario acaba de recuperar su contrasena con una temporal.
    debe_cambiar = datos_usuario.get("debe_cambiar_contrasena", False)
    if debe_cambiar or email.lower() in _emails_debe_cambiar:
        session["debe_cambiar_contrasena"] = True
        _emails_debe_cambiar.discard(email.lower())  # Ya no necesitamos rastrearlo
        flash("Debe cambiar su contrasena antes de continuar.", "warning")
        return redirect(url_for("auth.cambiar_contrasena"))

    # Paso 11: Login exitoso, redirigir al inicio
    flash(f"Bienvenido, {session.get('nombre_usuario', email)}", "success")  # "success" = alerta verde
    return redirect(url_for("home.index"))


# ══════════════════════════════════════════════════════════════
# RUTA: /logout - Cerrar sesion
# ══════════════════════════════════════════════════════════════
@bp.route("/logout")
def logout():
    """
    Cierra la sesion del usuario.
    session.clear() elimina TODOS los datos de la sesion.
    Luego redirige al login.
    """
    session.clear()
    return redirect(url_for("auth.login"))


# ══════════════════════════════════════════════════════════════
# RUTA: /cambiar-contrasena (GET) - Mostrar formulario
# ══════════════════════════════════════════════════════════════
@bp.route("/cambiar-contrasena", methods=["GET"])
def cambiar_contrasena():
    """Muestra el formulario para cambiar contrasena."""
    return render_template("pages/cambiar_contrasena.html")


# ══════════════════════════════════════════════════════════════
# RUTA: /cambiar-contrasena (POST) - Procesar cambio
# ══════════════════════════════════════════════════════════════
@bp.route("/cambiar-contrasena", methods=["POST"])
def cambiar_contrasena_post():
    """
    Procesa el cambio de contrasena.

    Pasos:
      1. Leer contrasena actual, nueva y confirmacion del formulario
      2. Verificar que nueva y confirmacion coincidan
      3. Validar requisitos de la nueva contrasena (6 chars, mayuscula, numero)
      4. Llamar a la API para actualizar (con ?encriptar=contrasena para BCrypt)
      5. Si OK: quitar el flag debe_cambiar y redirigir al inicio
    """
    email = session.get("usuario", "")
    actual = request.form.get("actual", "")
    nueva = request.form.get("nueva", "")
    confirmar = request.form.get("confirmar", "")

    # Verificar que las contrasenas coincidan
    if nueva != confirmar:
        flash("Las contrasenas no coinciden.", "danger")
        return render_template("pages/cambiar_contrasena.html")

    # Validar requisitos de seguridad
    error = validar_contrasena(nueva)
    if error:
        flash(error, "danger")
        return render_template("pages/cambiar_contrasena.html")

    # Actualizar en la BD (la API encripta con BCrypt gracias a ?encriptar=contrasena)
    exito, mensaje = auth.actualizar_contrasena(email, nueva)
    if exito:
        # Quitar el flag de "debe cambiar" de la sesion
        session.pop("debe_cambiar_contrasena", None)
        flash("Contrasena actualizada exitosamente.", "success")
        return redirect(url_for("home.index"))

    flash(f"Error al actualizar: {mensaje}", "danger")
    return render_template("pages/cambiar_contrasena.html")


# ══════════════════════════════════════════════════════════════
# RUTA: /recuperar-contrasena (GET) - Mostrar formulario
# ══════════════════════════════════════════════════════════════
@bp.route("/recuperar-contrasena", methods=["GET"])
def recuperar_contrasena():
    """Muestra el formulario para recuperar contrasena."""
    return render_template("pages/recuperar_contrasena.html")


# ══════════════════════════════════════════════════════════════
# RUTA: /recuperar-contrasena (POST) - Generar contrasena temporal
# ══════════════════════════════════════════════════════════════
@bp.route("/recuperar-contrasena", methods=["POST"])
def recuperar_contrasena_post():
    """
    Recupera la contrasena de un usuario.

    Pasos:
      1. Buscar el usuario por email en la BD
      2. Si no existe -> error
      3. Generar una contrasena temporal aleatoria (8 caracteres)
      4. Guardarla en la BD (encriptada con BCrypt)
      5. Marcar el email para forzar cambio en el proximo login
      6. Enviar la temporal por correo electronico (si SMTP esta configurado)

    NOTA: La contrasena temporal se genera en texto plano, se envia al usuario
    por email, y se guarda encriptada en la BD. El usuario la usa para entrar
    una sola vez, luego se le obliga a crear una contrasena definitiva.
    """
    email = request.form.get("email", "").strip()
    if not email:
        flash("Ingrese su correo electronico.", "danger")
        return render_template("pages/recuperar_contrasena.html")

    # Buscar si el usuario existe en la BD
    datos_usuario = auth.obtener_datos_usuario(email)
    if not datos_usuario:
        flash("No se encontro una cuenta con ese correo.", "danger")
        return render_template("pages/recuperar_contrasena.html")

    # Generar contrasena temporal aleatoria de 8 caracteres.
    # Garantiza al menos: 1 mayuscula, 1 minuscula, 1 digito + 5 aleatorios.
    # Ejemplo resultado: "Ak7xPm2q"
    pwd = "".join([random.choice(string.ascii_uppercase),    # 1 mayuscula (A-Z)
                   random.choice(string.ascii_lowercase),    # 1 minuscula (a-z)
                   random.choice(string.digits)]             # 1 digito (0-9)
                  + random.choices(string.ascii_letters + string.digits, k=5))  # 5 aleatorios

    # Guardar la contrasena temporal en la BD (encriptada con BCrypt)
    exito, mensaje = auth.actualizar_contrasena(email, pwd)
    if not exito:
        flash(f"Error: {mensaje}", "danger")
        return render_template("pages/recuperar_contrasena.html")

    # Marcar para forzar cambio de contrasena en el proximo login
    _emails_debe_cambiar.add(email.lower())

    # Intentar enviar la contrasena temporal por correo electronico.
    # Si SMTP no esta configurado en config.py, avisara pero la contrasena
    # ya fue cambiada (el admin deberia comunicarla manualmente).
    ok_email, msg_email = enviar_contrasena_temporal(email, pwd)

    if ok_email:
        flash("Se envio una contrasena temporal a su correo.", "success")
    else:
        flash(f"Contrasena restablecida pero no se pudo enviar el correo: {msg_email}", "warning")

    return redirect(url_for("auth.login"))
