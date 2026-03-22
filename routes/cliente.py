"""
cliente.py - Blueprint CRUD para la tabla Cliente.

Campos: id (PK, auto), credito, fkcodpersona (FK), fkcodempresa (FK, opcional)
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.api_service import ApiService

bp = Blueprint('cliente', __name__)
api = ApiService()
TABLA = 'cliente'
CLAVE = 'id'


@bp.route('/cliente')
def index():
    limite = request.args.get('limite', type=int)
    accion = request.args.get('accion', '')
    valor_clave = request.args.get('clave', '')

    registros = api.listar(TABLA, limite)
    personas = api.listar('persona')
    empresas = api.listar('empresa')

    mostrar_formulario = accion in ('nuevo', 'editar')
    editando = accion == 'editar'

    registro = None
    if editando and valor_clave:
        registro = next(
            (r for r in registros if str(r.get(CLAVE)) == valor_clave), None
        )

    mapa_personas = {str(p.get('codigo', '')): p.get('nombre', 'Sin nombre') for p in personas}
    mapa_empresas = {str(e.get('codigo', '')): e.get('nombre', 'Sin nombre') for e in empresas}

    return render_template('pages/cliente.html',
        registros=registros, mostrar_formulario=mostrar_formulario,
        editando=editando, registro=registro, limite=limite,
        personas=personas, empresas=empresas,
        mapa_personas=mapa_personas, mapa_empresas=mapa_empresas
    )


@bp.route('/cliente/crear', methods=['POST'])
def crear():
    datos = {
        'credito': request.form.get('credito', '0'),
        'fkcodpersona': request.form.get('fkcodpersona', ''),
        'fkcodempresa': request.form.get('fkcodempresa', '') or None
    }
    exito, mensaje = api.crear(TABLA, datos)
    flash(mensaje, 'success' if exito else 'danger')
    return redirect(url_for('cliente.index'))


@bp.route('/cliente/actualizar', methods=['POST'])
def actualizar():
    valor = request.form.get('id', '')
    datos = {
        'credito': request.form.get('credito', '0'),
        'fkcodpersona': request.form.get('fkcodpersona', ''),
        'fkcodempresa': request.form.get('fkcodempresa', '') or None
    }
    exito, mensaje = api.actualizar(TABLA, CLAVE, valor, datos)
    flash(mensaje, 'success' if exito else 'danger')
    return redirect(url_for('cliente.index'))


@bp.route('/cliente/eliminar', methods=['POST'])
def eliminar():
    valor = request.form.get('id', '')
    exito, mensaje = api.eliminar(TABLA, CLAVE, valor)
    flash(mensaje, 'success' if exito else 'danger')
    return redirect(url_for('cliente.index'))
