"""
app.py - Punto de entrada de la aplicacion Flask.
"""

from flask import Flask
from config import SECRET_KEY

# Crear la aplicacion Flask
app = Flask(__name__)
app.secret_key = SECRET_KEY

# (Aqui se registraran los Blueprints en pasos posteriores)

if __name__ == '__main__':
    app.run(debug=True, port=5300)
