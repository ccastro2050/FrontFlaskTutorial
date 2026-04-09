"""
app.py - Punto de entrada de la aplicacion Flask.

COMO FUNCIONA LA AUTENTICACION EN ESTA APP:
============================================
1. Se importa el middleware de autenticacion (middleware/auth_middleware.py)
2. Se registra con crear_middleware(app) ANTES de los blueprints
3. El middleware intercepta CADA request y verifica:
   - Si es una ruta publica (/login, /static) -> deja pasar
   - Si no tiene sesion -> redirige a /login
   - Si la ruta no esta permitida para su rol -> muestra error 403

ORDEN IMPORTANTE:
=================
  1. Crear app Flask
  2. Registrar middleware (crear_middleware) <-- ANTES de los blueprints
  3. Registrar blueprints (auth_bp primero, luego los demas)

Si el middleware se registra DESPUES de los blueprints, las rutas
podrian ejecutarse sin verificar permisos.

ARCHIVOS RELACIONADOS:
======================
  - middleware/auth_middleware.py  -> El middleware que verifica permisos
  - routes/auth.py                -> Las rutas de login/logout/cambiar contrasena
  - services/auth_service.py      -> Servicio que habla con la API para autenticar
  - services/email_service.py     -> Envio de correo para contrasena temporal
  - config.py                     -> Configuracion (API URL, SMTP, secret key)
"""

from flask import Flask
from config import SECRET_KEY

# Crear la aplicacion Flask
app = Flask(__name__)

# ─── PASO 1: Configurar middleware de autenticacion ────────────
# El middleware se registra ANTES de los blueprints para que
# intercepte todas las peticiones y verifique permisos.
from middleware.auth_middleware import crear_middleware
app.secret_key = SECRET_KEY    # Clave para encriptar la cookie de sesion
crear_middleware(app)           # Registra @app.before_request y @app.context_processor

# ─── PASO 2: Registrar Blueprints ─────────────────────────────
# auth_bp se registra PRIMERO porque define las rutas /login, /logout, etc.
# que el middleware necesita para redirigir usuarios no autenticados.
from routes.home import bp as home_bp
from routes.producto import bp as producto_bp

from routes.usuario import bp as usuario_bp
from routes.auth import bp as auth_bp
app.register_blueprint(auth_bp)       # /login, /logout, /cambiar-contrasena, /recuperar-contrasena

app.register_blueprint(home_bp)       # /
app.register_blueprint(producto_bp)   # /producto
app.register_blueprint(usuario_bp)    # /usuario

from routes.persona import bp as persona_bp

from routes.cliente import bp as cliente_bp
app.register_blueprint(persona_bp)    # /persona
app.register_blueprint(cliente_bp)    # /cliente


from routes.rol import bp as rol_bp

app.register_blueprint(rol_bp)        # /rol

from routes.empresa import bp as empresa_bp

from routes.vendedor import bp as vendedor_bp
app.register_blueprint(empresa_bp)    # /empresa
app.register_blueprint(vendedor_bp)   # /vendedor



from routes.ruta import bp as ruta_bp

app.register_blueprint(ruta_bp)       # /ruta

from routes.factura import bp as factura_bp
app.register_blueprint(factura_bp)    # /factura

if __name__ == '__main__':
    app.run(debug=True, port=5300)
