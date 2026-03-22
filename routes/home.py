"""
home.py - Blueprint para la pagina de inicio.
"""

from flask import Blueprint, render_template
from services.api_service import ApiService
import requests

bp = Blueprint('home', __name__)
api = ApiService()


@bp.route('/')
def index():
    diagnostico = None
    try:
        url = f"{api.base_url}/api/diagnostico/conexion"
        respuesta = requests.get(url, timeout=3)
        if respuesta.ok:
            diagnostico = respuesta.json()
    except Exception:
        pass

    return render_template('pages/home.html', diagnostico=diagnostico)
