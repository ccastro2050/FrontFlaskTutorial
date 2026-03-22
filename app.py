"""
app.py - Punto de entrada de la aplicacion Flask.
"""

from flask import Flask
from config import SECRET_KEY

# Crear la aplicacion Flask
app = Flask(__name__)
app.secret_key = SECRET_KEY

# Registrar Blueprints
from routes.home import bp as home_bp
from routes.producto import bp as producto_bp

from routes.usuario import bp as usuario_bp
app.register_blueprint(home_bp)
app.register_blueprint(producto_bp)
app.register_blueprint(usuario_bp)

from routes.persona import bp as persona_bp

from routes.rol import bp as rol_bp
app.register_blueprint(persona_bp)
app.register_blueprint(rol_bp)

from routes.empresa import bp as empresa_bp
app.register_blueprint(empresa_bp)



if __name__ == '__main__':
    app.run(debug=True, port=5300)
