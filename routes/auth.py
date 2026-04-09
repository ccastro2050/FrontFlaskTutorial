"""Rutas de autenticacion: login, logout, cambiar y recuperar contrasena.

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

SIN_LIMITE = 999999

bp = Blueprint("auth", __name__)
auth = AuthService()

_emails_debe_cambiar = set()


def validar_contrasena(pwd):
    if len(pwd) < 6:
        return "La contrasena debe tener al menos 6 caracteres."
    if not any(c.isupper() for c in pwd):
        return "Debe incluir al menos una letra mayuscula."
    if not any(c.isdigit() for c in pwd):
        return "Debe incluir al menos un numero."
    if pwd in ("123", "1234", "12345", "123456"):
        return "No puede usar una contrasena trivial."
    return None


@bp.route("/login", methods=["GET"])
def login():
    if session.get("usuario"):
        return redirect(url_for("home.index"))
    return render_template("pages/login.html")


@bp.route("/login", methods=["POST"])
def login_post():
    email = request.form.get("email", "").strip()
    contrasena = request.form.get("contrasena", "")
    if not email or not contrasena:
        flash("Ingrese email y contrasena.", "danger")
        return render_template("pages/login.html")

    exito, datos = auth.login(email, contrasena)
    if not exito:
        flash(datos.get("mensaje", "Error de autenticacion."), "danger")
        return render_template("pages/login.html")

    roles = auth.obtener_roles_usuario(email)
    if not roles:
        flash("El usuario no tiene roles asignados.", "warning")
        return render_template("pages/login.html")

    rutas_permitidas = auth.obtener_rutas_permitidas(roles)
    datos_usuario = auth.obtener_datos_usuario(email)

    session["usuario"] = email
    session["nombre_usuario"] = datos_usuario.get("nombre", email)
    session["token"] = datos.get("token", "")
    session["roles"] = roles
    session["rutas_permitidas"] = list(rutas_permitidas)

    debe_cambiar = datos_usuario.get("debe_cambiar_contrasena", False)
    if debe_cambiar or email.lower() in _emails_debe_cambiar:
        session["debe_cambiar_contrasena"] = True
        _emails_debe_cambiar.discard(email.lower())
        flash("Debe cambiar su contrasena antes de continuar.", "warning")
        return redirect(url_for("auth.cambiar_contrasena"))

    flash(f"Bienvenido, {session.get('nombre_usuario', email)}", "success")
    return redirect(url_for("home.index"))


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))


@bp.route("/cambiar-contrasena", methods=["GET"])
def cambiar_contrasena():
    return render_template("pages/cambiar_contrasena.html")


@bp.route("/cambiar-contrasena", methods=["POST"])
def cambiar_contrasena_post():
    email = session.get("usuario", "")
    actual = request.form.get("actual", "")
    nueva = request.form.get("nueva", "")
    confirmar = request.form.get("confirmar", "")

    if nueva != confirmar:
        flash("Las contrasenas no coinciden.", "danger")
        return render_template("pages/cambiar_contrasena.html")

    error = validar_contrasena(nueva)
    if error:
        flash(error, "danger")
        return render_template("pages/cambiar_contrasena.html")

    exito, mensaje = auth.actualizar_contrasena(email, nueva)
    if exito:
        session.pop("debe_cambiar_contrasena", None)
        flash("Contrasena actualizada exitosamente.", "success")
        return redirect(url_for("home.index"))

    flash(f"Error al actualizar: {mensaje}", "danger")
    return render_template("pages/cambiar_contrasena.html")


@bp.route("/recuperar-contrasena", methods=["GET"])
def recuperar_contrasena():
    return render_template("pages/recuperar_contrasena.html")


@bp.route("/recuperar-contrasena", methods=["POST"])
def recuperar_contrasena_post():
    email = request.form.get("email", "").strip()
    if not email:
        flash("Ingrese su correo electronico.", "danger")
        return render_template("pages/recuperar_contrasena.html")

    datos_usuario = auth.obtener_datos_usuario(email)
    if not datos_usuario:
        flash("No se encontro una cuenta con ese correo.", "danger")
        return render_template("pages/recuperar_contrasena.html")

    pwd = "".join([random.choice(string.ascii_uppercase), random.choice(string.ascii_lowercase),
                   random.choice(string.digits)] + random.choices(string.ascii_letters + string.digits, k=5))

    exito, mensaje = auth.actualizar_contrasena(email, pwd)
    if not exito:
        flash(f"Error: {mensaje}", "danger")
        return render_template("pages/recuperar_contrasena.html")

    _emails_debe_cambiar.add(email.lower())
    ok_email, msg_email = enviar_contrasena_temporal(email, pwd)

    if ok_email:
        flash("Se envio una contrasena temporal a su correo.", "success")
    else:
        flash(f"Contrasena restablecida pero no se pudo enviar el correo: {msg_email}", "warning")

    return redirect(url_for("auth.login"))
