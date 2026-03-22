"""
ruta.py - Blueprint CRUD para la tabla Ruta.

Campos: ruta (PK), descripcion
Nota: Blueprint se llama 'ruta_page' para no confundir con el campo 'ruta'.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.api_service import ApiService

bp = Blueprint('ruta_page', __name__)
api = ApiService()
TABLA = 'ruta'
CLAVE = 'ruta'


@bp.route('/ruta')
def index():
    limite = request.args.get('limite', type=int)
    accion = request.args.get('accion', '')
    valor_clave = request.args.get('clave', '')

    registros = api.listar(TABLA, limite)
    mostrar_formulario = accion in ('nuevo', 'editar')
    editando = accion == 'editar'

    registro = None
    if editando and valor_clave:
        registro = next(
            (r for r in registros if str(r.get(CLAVE)) == valor_clave), None
        )

    return render_template('pages/ruta.html',
        registros=registros, mostrar_formulario=mostrar_formulario,
        editando=editando, registro=registro, limite=limite
    )


@bp.route('/ruta/crear', methods=['POST'])
def crear():
    datos = {
        'ruta':        request.form.get('ruta', ''),
        'descripcion': request.form.get('descripcion', '')
    }
    exito, mensaje = api.crear(TABLA, datos)
    flash(mensaje, 'success' if exito else 'danger')
    return redirect(url_for('ruta_page.index'))


@bp.route('/ruta/actualizar', methods=['POST'])
def actualizar():
    valor = request.form.get('ruta', '')
    datos = {
        'descripcion': request.form.get('descripcion', '')
    }
    exito, mensaje = api.actualizar(TABLA, CLAVE, valor, datos)
    flash(mensaje, 'success' if exito else 'danger')
    return redirect(url_for('ruta_page.index'))


@bp.route('/ruta/eliminar', methods=['POST'])
def eliminar():
    valor = request.form.get('ruta', '')
    exito, mensaje = api.eliminar(TABLA, CLAVE, valor)
    flash(mensaje, 'success' if exito else 'danger')
    return redirect(url_for('ruta_page.index'))
