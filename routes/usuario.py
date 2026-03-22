"""
usuario.py - Blueprint CRUD para la tabla Usuario.

Campos: email (PK), contrasena
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.api_service import ApiService

bp = Blueprint('usuario', __name__)
api = ApiService()
TABLA = 'usuario'
CLAVE = 'email'


@bp.route('/usuario')
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

    return render_template('pages/usuario.html',
        registros=registros, mostrar_formulario=mostrar_formulario,
        editando=editando, registro=registro, limite=limite
    )


@bp.route('/usuario/crear', methods=['POST'])
def crear():
    datos = {
        'email':      request.form.get('email', ''),
        'contrasena': request.form.get('contrasena', '')
    }
    exito, mensaje = api.crear(TABLA, datos)
    flash(mensaje, 'success' if exito else 'danger')
    return redirect(url_for('usuario.index'))


@bp.route('/usuario/actualizar', methods=['POST'])
def actualizar():
    valor = request.form.get('email', '')
    datos = {
        'contrasena': request.form.get('contrasena', '')
    }
    exito, mensaje = api.actualizar(TABLA, CLAVE, valor, datos)
    flash(mensaje, 'success' if exito else 'danger')
    return redirect(url_for('usuario.index'))


@bp.route('/usuario/eliminar', methods=['POST'])
def eliminar():
    valor = request.form.get('email', '')
    exito, mensaje = api.eliminar(TABLA, CLAVE, valor)
    flash(mensaje, 'success' if exito else 'danger')
    return redirect(url_for('usuario.index'))
