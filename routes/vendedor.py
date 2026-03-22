"""
vendedor.py - Blueprint CRUD para la tabla Vendedor.

Campos: id (PK, auto), carnet, direccion, fkcodpersona (FK)
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.api_service import ApiService

bp = Blueprint('vendedor', __name__)
api = ApiService()
TABLA = 'vendedor'
CLAVE = 'id'


@bp.route('/vendedor')
def index():
    limite = request.args.get('limite', type=int)
    accion = request.args.get('accion', '')
    valor_clave = request.args.get('clave', '')

    registros = api.listar(TABLA, limite)
    personas = api.listar('persona')

    mostrar_formulario = accion in ('nuevo', 'editar')
    editando = accion == 'editar'

    registro = None
    if editando and valor_clave:
        registro = next(
            (r for r in registros if str(r.get(CLAVE)) == valor_clave), None
        )

    mapa_personas = {str(p.get('codigo', '')): p.get('nombre', 'Sin nombre') for p in personas}

    return render_template('pages/vendedor.html',
        registros=registros, mostrar_formulario=mostrar_formulario,
        editando=editando, registro=registro, limite=limite,
        personas=personas, mapa_personas=mapa_personas
    )


@bp.route('/vendedor/crear', methods=['POST'])
def crear():
    datos = {
        'carnet': request.form.get('carnet', ''),
        'direccion': request.form.get('direccion', ''),
        'fkcodpersona': request.form.get('fkcodpersona', '')
    }
    exito, mensaje = api.crear(TABLA, datos)
    flash(mensaje, 'success' if exito else 'danger')
    return redirect(url_for('vendedor.index'))


@bp.route('/vendedor/actualizar', methods=['POST'])
def actualizar():
    valor = request.form.get('id', '')
    datos = {
        'carnet': request.form.get('carnet', ''),
        'direccion': request.form.get('direccion', ''),
        'fkcodpersona': request.form.get('fkcodpersona', '')
    }
    exito, mensaje = api.actualizar(TABLA, CLAVE, valor, datos)
    flash(mensaje, 'success' if exito else 'danger')
    return redirect(url_for('vendedor.index'))


@bp.route('/vendedor/eliminar', methods=['POST'])
def eliminar():
    valor = request.form.get('id', '')
    exito, mensaje = api.eliminar(TABLA, CLAVE, valor)
    flash(mensaje, 'success' if exito else 'danger')
    return redirect(url_for('vendedor.index'))
