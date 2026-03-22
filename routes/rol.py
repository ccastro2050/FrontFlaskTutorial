"""
rol.py - Blueprint CRUD para la tabla Rol.

Campos: id (PK, int), nombre
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.api_service import ApiService

bp = Blueprint('rol', __name__)
api = ApiService()
TABLA = 'rol'
CLAVE = 'id'


@bp.route('/rol')
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
            (r for r in registros if str(r.get(CLAVE)) == str(valor_clave)), None
        )

    return render_template('pages/rol.html',
        registros=registros, mostrar_formulario=mostrar_formulario,
        editando=editando, registro=registro, limite=limite
    )


@bp.route('/rol/crear', methods=['POST'])
def crear():
    datos = {
        'id':     request.form.get('id', 0, type=int),
        'nombre': request.form.get('nombre', '')
    }
    exito, mensaje = api.crear(TABLA, datos)
    flash(mensaje, 'success' if exito else 'danger')
    return redirect(url_for('rol.index'))


@bp.route('/rol/actualizar', methods=['POST'])
def actualizar():
    valor = request.form.get('id', '')
    datos = {
        'nombre': request.form.get('nombre', '')
    }
    exito, mensaje = api.actualizar(TABLA, CLAVE, valor, datos)
    flash(mensaje, 'success' if exito else 'danger')
    return redirect(url_for('rol.index'))


@bp.route('/rol/eliminar', methods=['POST'])
def eliminar():
    valor = request.form.get('id', '')
    exito, mensaje = api.eliminar(TABLA, CLAVE, valor)
    flash(mensaje, 'success' if exito else 'danger')
    return redirect(url_for('rol.index'))
