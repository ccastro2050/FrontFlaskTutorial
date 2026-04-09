"""
auth_middleware.py - Middleware de autenticacion y control de acceso.

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
       ├── Es ruta publica (/login, /static, etc)?  -> SI: dejar pasar
       |
       ├── Tiene sesion activa?  -> NO: redirigir a /login
       |
       ├── Debe cambiar contrasena?  -> SI: redirigir a /cambiar-contrasena
       |
       ├── Es la pagina de inicio (/)?  -> SI: dejar pasar (siempre accesible)
       |
       ├── Tiene rutas_permitidas configuradas?  -> NO: dejar pasar (sistema nuevo)
       |
       ├── La ruta esta en sus rutas_permitidas?  -> SI: dejar pasar
       |
       └── NO esta permitida  -> Mostrar pagina "Acceso Denegado" (403)

QUE ES EL CONTEXT PROCESSOR:
=============================
Un context_processor inyecta variables en TODAS las templates Jinja2 automaticamente.
En vez de pasar "usuario", "roles", etc. manualmente en cada render_template(),
el context_processor las hace disponibles en todas las templates.

Ejemplo en cualquier template:
  {{ usuario }}              -> email del usuario logueado
  {{ nombre_usuario }}       -> nombre para mostrar
  {{ roles }}                -> lista de roles
  {% if "/producto" in rutas_permitidas %}  -> condicional para mostrar/ocultar menu
"""

from flask import session, redirect, url_for, flash, request, render_template


# Lista de rutas que NO requieren autenticacion.
# Cualquier URL que empiece con alguna de estas se deja pasar sin verificar.
# Ejemplo: "/static/css/app.css" empieza con "/static" -> es publica.
RUTAS_PUBLICAS = ['/login', '/logout', '/static', '/recuperar-contrasena', '/ayuda']


def crear_middleware(app):
    """
    Registra el middleware de autenticacion en la aplicacion Flask.

    Se llama desde app.py asi:
        from middleware.auth_middleware import crear_middleware
        crear_middleware(app)

    Esto registra dos funciones:
      1. before_request: se ejecuta ANTES de cada peticion
      2. context_processor: inyecta variables en todas las templates
    """

    # ──────────────────────────────────────────────────────────
    # BEFORE_REQUEST: Se ejecuta antes de CADA peticion HTTP
    # ──────────────────────────────────────────────────────────
    @app.before_request
    def verificar_autenticacion():
        """
        Verifica si el usuario puede acceder a la ruta solicitada.
        Si retorna None (no retorna nada), Flask continua con la ruta normal.
        Si retorna un redirect o render_template, Flask usa esa respuesta
        en vez de la ruta original (bloquea el acceso).
        """

        # 1. RUTAS PUBLICAS: no requieren autenticacion
        #    Ejemplo: /login, /static/css/app.css, /ayuda
        if any(request.path.startswith(r) for r in RUTAS_PUBLICAS):
            return  # return sin valor = dejar pasar

        # 2. NO HAY SESION: el usuario no ha hecho login
        #    session.get("usuario") retorna None si no existe
        if not session.get("usuario"):
            return redirect(url_for("auth.login"))

        # 3. DEBE CAMBIAR CONTRASENA: forzar antes de hacer cualquier cosa
        #    Esto se activa cuando se recupera una contrasena con temporal
        if session.get("debe_cambiar_contrasena") and request.path != "/cambiar-contrasena":
            return redirect(url_for("auth.cambiar_contrasena"))

        # 4. PAGINA DE INICIO: siempre accesible para usuarios autenticados
        #    No tendria sentido bloquear la pagina principal
        if request.path == "/":
            return

        # 5. CONTROL DE ACCESO POR RUTA
        #    Aqui es donde se verifica si el usuario tiene permiso para
        #    acceder a la pagina solicitada, segun sus roles.
        rutas_permitidas = set(session.get("rutas_permitidas", []))

        if not rutas_permitidas:
            # Si no hay rutas configuradas en el sistema, permitir todo.
            # Esto pasa cuando el sistema es nuevo y no se han creado
            # las tablas ruta/rutarol, o no se han asignado rutas a roles.
            return

        # Verificar si la ruta actual esta en las rutas permitidas.
        # Tambien verifica sub-rutas: si "/producto" esta permitida,
        # entonces "/producto/editar" tambien lo esta.
        ruta_actual = request.path
        permitida = False
        for ruta in rutas_permitidas:
            if ruta_actual == ruta or ruta_actual.startswith(ruta + "/"):
                permitida = True
                break

        if not permitida:
            # El usuario no tiene permiso -> mostrar pagina de error 403
            return render_template("pages/sin_acceso.html"), 403

    # ──────────────────────────────────────────────────────────
    # CONTEXT PROCESSOR: Inyecta variables en todas las templates
    # ──────────────────────────────────────────────────────────
    @app.context_processor
    def inyectar_sesion():
        """
        Hace que estas variables esten disponibles en TODAS las templates
        Jinja2 sin necesidad de pasarlas manualmente en render_template().

        En cualquier template puedes usar:
          {{ usuario }}          -> "juan@mail.com"
          {{ nombre_usuario }}   -> "Juan Perez"
          {{ roles }}            -> ["Vendedor", "Bodeguero"]

        Para mostrar/ocultar elementos del menu segun permisos:
          {% if "/producto" in rutas_permitidas %}
              <a href="/producto">Productos</a>
          {% endif %}
        """
        return {
            "usuario": session.get("usuario", ""),
            "nombre_usuario": session.get("nombre_usuario", ""),
            "roles": session.get("roles", []),
            "rutas_permitidas": set(session.get("rutas_permitidas", [])),
        }
