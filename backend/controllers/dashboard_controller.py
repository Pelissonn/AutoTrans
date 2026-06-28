from flask import Blueprint, render_template

from models import Categoria

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
def bem_vindo():
    return render_template("bem_vindo.html")


@dashboard_bp.route("/inicio")
def index():
    categorias = Categoria.listar()
    return render_template("index.html", categorias=categorias)


@dashboard_bp.route("/categoria/<int:categoria_id>/material")
def material(categoria_id):
    categoria = Categoria.query.get(categoria_id)
    return render_template("material.html", categoria=categoria)
