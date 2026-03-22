"""
config.py - Configuracion centralizada de la aplicacion Flask.
"""

# URL base de la API REST que consume este frontend.
# La API generica en C# corre en el puerto 5035.
API_BASE_URL = "http://localhost:5035"

# Clave secreta para el manejo de sesiones y mensajes flash.
SECRET_KEY = "clave-secreta-flask-frontend-2024"
