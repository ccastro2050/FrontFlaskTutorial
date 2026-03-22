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
app.register_blueprint(home_bp)
app.register_blueprint(producto_bp)

if __name__ == '__main__':
    app.run(debug=True, port=5300)
