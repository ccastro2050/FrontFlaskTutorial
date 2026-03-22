"""
producto.py - Blueprint CRUD para la tabla Producto.

Campos: codigo (PK), nombre, stock (int), valorunitario (float)
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.api_service import ApiService

bp = Blueprint('producto', __name__)
api = ApiService()
TABLA = 'producto'
CLAVE = 'codigo'


@bp.route('/producto')
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
            (r for r in registros if str(r.get(CLAVE)) == valor_clave),
            None
        )

    return render_template('pages/producto.html',
        registros=registros,
        mostrar_formulario=mostrar_formulario,
        editando=editando,
        registro=registro,
        limite=limite
    )


@bp.route('/producto/crear', methods=['POST'])
def crear():
    datos = {
        'codigo':        request.form.get('codigo', ''),
        'nombre':        request.form.get('nombre', ''),
        'stock':         request.form.get('stock', 0, type=int),
        'valorunitario': request.form.get('valorunitario', 0, type=float)
    }

    exito, mensaje = api.crear(TABLA, datos)
    flash(mensaje, 'success' if exito else 'danger')
    return redirect(url_for('producto.index'))


@bp.route('/producto/actualizar', methods=['POST'])
def actualizar():
    valor = request.form.get('codigo', '')
    datos = {
        'nombre':        request.form.get('nombre', ''),
        'stock':         request.form.get('stock', 0, type=int),
        'valorunitario': request.form.get('valorunitario', 0, type=float)
    }

    exito, mensaje = api.actualizar(TABLA, CLAVE, valor, datos)
    flash(mensaje, 'success' if exito else 'danger')
    return redirect(url_for('producto.index'))


@bp.route('/producto/eliminar', methods=['POST'])
def eliminar():
    valor = request.form.get('codigo', '')
    exito, mensaje = api.eliminar(TABLA, CLAVE, valor)
    flash(mensaje, 'success' if exito else 'danger')
    return redirect(url_for('producto.index'))
