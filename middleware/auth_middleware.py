"""Middleware de autenticacion y control de acceso por rutas.

QUE ES UN MIDDLEWARE:
=====================
Un middleware es codigo que se ejecuta ANTES de cada request (peticion HTTP).
En Flask se implementa con @app.before_request.

Cada vez que un usuario visita cualquier pagina (/, /producto, /cliente, etc.),
este codigo se ejecuta PRIMERO y decide si el usuario puede continuar o no.

FLUJO DE CADA REQUEST:
======================
  Usuario visita /producto
       |
       v
  [before_request] <-- ESTE MIDDLEWARE
       |
       +-- Es ruta publica (/login, /static, etc)?  -> SI: dejar pasar
       |
       +-- Tiene sesion activa?  -> NO: redirigir a /login
       |
       +-- Debe cambiar contrasena?  -> SI: redirigir a /cambiar-contrasena
       |
       +-- Es la pagina de inicio (/)?  -> SI: dejar pasar (siempre accesible)
       |
       +-- Tiene rutas_permitidas configuradas?  -> NO: dejar pasar (sistema nuevo)
       |
       +-- La ruta esta en sus rutas_permitidas?  -> SI: dejar pasar
       |
       +-- NO esta permitida  -> Mostrar pagina "Acceso Denegado" (403)

QUE ES EL CONTEXT PROCESSOR:
=============================
Un context_processor inyecta variables en TODAS las templates Jinja2 automaticamente.
En vez de pasar "usuario", "roles", etc. manualmente en cada render_template(),
el context_processor las hace disponibles en todas las templates.

Ejemplo en cualquier template:
  {{ usuario }}              -> email del usuario logueado
  {{ nombre_usuario }}       -> nombre para mostrar
  {{ roles }}                -> lista de roles
  {%% if "/producto" in rutas_permitidas %%}  -> condicional para mostrar/ocultar menu
"""

from flask import session, redirect, url_for, flash, request, render_template


RUTAS_PUBLICAS = ['/login', '/logout', '/static', '/recuperar-contrasena', '/ayuda']


def crear_middleware(app):
    """Registra before_request con enforcement real de rutas_permitidas."""

    @app.before_request
    def verificar_autenticacion():
        # 1. Rutas publicas: no requieren autenticacion
        if any(request.path.startswith(r) for r in RUTAS_PUBLICAS):
            return

        # 2. No hay sesion: redirigir a login
        if not session.get("usuario"):
            return redirect(url_for("auth.login"))

        # 3. Debe cambiar contrasena: forzar cambio
        if session.get("debe_cambiar_contrasena") and request.path != "/cambiar-contrasena":
            return redirect(url_for("auth.cambiar_contrasena"))

        # 4. Control de acceso por ruta
        #    La ruta "/" (home) siempre es accesible para usuarios autenticados
        if request.path == "/":
            return

        rutas_permitidas = set(session.get("rutas_permitidas", []))
        if not rutas_permitidas:
            # Si no hay rutas asignadas, permitir (sistema sin admin_rutas configurado)
            return

        # Verificar si la ruta actual (o su prefijo) esta permitida
        ruta_actual = request.path
        permitida = False
        for ruta in rutas_permitidas:
            if ruta_actual == ruta or ruta_actual.startswith(ruta + "/"):
                permitida = True
                break

        if not permitida:
            return render_template("pages/sin_acceso.html"), 403


    @app.context_processor
    def inyectar_sesion():
        return {
            "usuario": session.get("usuario", ""),
            "nombre_usuario": session.get("nombre_usuario", ""),
            "roles": session.get("roles", []),
            "rutas_permitidas": set(session.get("rutas_permitidas", [])),
        }
