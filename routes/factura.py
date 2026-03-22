"""
factura.py - Blueprint CRUD para Facturas con Stored Procedures.

Usa SPs para operaciones maestro-detalle (factura + productos).
"""

import json
from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.api_service import ApiService

bp = Blueprint('factura', __name__)
api = ApiService()


@bp.route('/factura')
def index():
    exito, datos = api.ejecutar_sp("sp_listar_facturas_y_productosporfactura", {
        "p_resultado": None
    })

    facturas = []
    if exito and isinstance(datos, dict):
        facturas = datos.get("facturas", [])
    elif exito and isinstance(datos, list):
        facturas = datos

    return render_template('pages/factura.html', facturas=facturas, vista='listar')


@bp.route('/factura/ver/<int:numero>')
def ver(numero):
    exito, datos = api.ejecutar_sp("sp_consultar_factura_y_productosporfactura", {
        "p_numero": numero,
        "p_resultado": None
    })

    factura = None
    if exito and isinstance(datos, dict):
        info = datos.get("factura", datos)
        info["productos"] = datos.get("productos", [])
        factura = info

    return render_template('pages/factura.html', factura=factura, vista='ver')


@bp.route('/factura/nueva')
def nueva():
    clientes = api.listar('cliente')
    vendedores = api.listar('vendedor')
    personas = api.listar('persona')
    productos = api.listar('producto')

    mapa_personas = {p['codigo']: p['nombre'] for p in personas}
    for cli in clientes:
        cli['nombre'] = mapa_personas.get(cli.get('fkcodpersona'), 'Sin nombre')
    for ven in vendedores:
        ven['nombre'] = mapa_personas.get(ven.get('fkcodpersona'), 'Sin nombre')

    return render_template('pages/factura.html',
        vista='formulario', editando=False,
        clientes=clientes, vendedores=vendedores,
        productos_disponibles=productos
    )


@bp.route('/factura/crear', methods=['POST'])
def crear():
    fkidcliente = request.form.get('fkidcliente', 0, type=int)
    fkidvendedor = request.form.get('fkidvendedor', 0, type=int)

    codigos = request.form.getlist('prod_codigo[]')
    cantidades = request.form.getlist('prod_cantidad[]')

    productos_lista = []
    for codigo, cantidad in zip(codigos, cantidades):
        if codigo and cantidad:
            productos_lista.append({"codigo": codigo, "cantidad": int(cantidad)})

    if not productos_lista:
        flash("Debe agregar al menos un producto.", "danger")
        return redirect(url_for('factura.nueva'))

    exito, datos = api.ejecutar_sp("sp_insertar_factura_y_productosporfactura", {
        "p_fkidcliente": fkidcliente,
        "p_fkidvendedor": fkidvendedor,
        "p_productos": json.dumps(productos_lista),
        "p_resultado": None
    })

    if exito:
        flash("Factura creada exitosamente.", "success")
    else:
        flash(f"Error al crear factura: {datos}", "danger")

    return redirect(url_for('factura.index'))


@bp.route('/factura/editar/<int:numero>')
def editar(numero):
    exito, datos = api.ejecutar_sp("sp_consultar_factura_y_productosporfactura", {
        "p_numero": numero,
        "p_resultado": None
    })

    factura = None
    if exito and isinstance(datos, dict):
        info = datos.get("factura", datos)
        info["productos"] = datos.get("productos", [])
        factura = info

    if not factura:
        flash("Factura no encontrada.", "danger")
        return redirect(url_for('factura.index'))

    clientes = api.listar('cliente')
    vendedores = api.listar('vendedor')
    personas = api.listar('persona')
    productos = api.listar('producto')

    mapa_personas = {p['codigo']: p['nombre'] for p in personas}
    for cli in clientes:
        cli['nombre'] = mapa_personas.get(cli.get('fkcodpersona'), 'Sin nombre')
    for ven in vendedores:
        ven['nombre'] = mapa_personas.get(ven.get('fkcodpersona'), 'Sin nombre')

    return render_template('pages/factura.html',
        vista='formulario', editando=True, factura=factura,
        clientes=clientes, vendedores=vendedores,
        productos_disponibles=productos
    )


@bp.route('/factura/actualizar', methods=['POST'])
def actualizar():
    numero = request.form.get('numero', 0, type=int)
    fkidcliente = request.form.get('fkidcliente', 0, type=int)
    fkidvendedor = request.form.get('fkidvendedor', 0, type=int)

    codigos = request.form.getlist('prod_codigo[]')
    cantidades = request.form.getlist('prod_cantidad[]')

    productos_lista = []
    for codigo, cantidad in zip(codigos, cantidades):
        if codigo and cantidad:
            productos_lista.append({"codigo": codigo, "cantidad": int(cantidad)})

    if not productos_lista:
        flash("Debe agregar al menos un producto.", "danger")
        return redirect(url_for('factura.editar', numero=numero))

    exito, datos = api.ejecutar_sp("sp_actualizar_factura_y_productosporfactura", {
        "p_numero": numero,
        "p_fkidcliente": fkidcliente,
        "p_fkidvendedor": fkidvendedor,
        "p_productos": json.dumps(productos_lista),
        "p_resultado": None
    })

    if exito:
        flash("Factura actualizada exitosamente.", "success")
    else:
        flash(f"Error al actualizar factura: {datos}", "danger")

    return redirect(url_for('factura.index'))


@bp.route('/factura/eliminar', methods=['POST'])
def eliminar():
    numero = request.form.get('numero', 0, type=int)

    exito, datos = api.ejecutar_sp("sp_borrar_factura_y_productosporfactura", {
        "p_numero": numero,
        "p_resultado": None
    })

    if exito:
        flash("Factura eliminada exitosamente.", "success")
    else:
        flash(f"Error al eliminar factura: {datos}", "danger")

    return redirect(url_for('factura.index'))
