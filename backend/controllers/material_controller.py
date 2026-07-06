from flask import Blueprint, render_template, request, redirect, url_for
from models import Material, Categoria 
from services.materiais.create_material_service import CadastrarMaterialService
from services.materiais.read_material_service import ListarMateriaisService
from services.materiais.update_material_service import EditarMaterialService
from services.materiais.delete_material_service import DeletarMaterialService

material_bp = Blueprint('material', __name__,url_prefix="/materiais")

@material_bp.route("/")
def listar():
    service = ListarMateriaisService()
    materiais = service.executar()
    return render_template("material/listar.html", materiais=materiais)

@material_bp.route("/cadastrar", methods=["GET", "POST"])
def cadastrar():
    if request.method == "GET":
        categorias = Categoria.query.all() 
        return render_template("material/cadastrar.html", categorias=categorias)
    
    conteudo = request.form.get("conteudo")
    url = request.form.get("url")
    categoria_id = request.form.get("categoria_id")
    
    service = CadastrarMaterialService()
    try:
        service.executar(conteudo, url, categoria_id)
        return redirect(url_for("material.listar"))
    except ValueError as e:
        categorias = Categoria.query.all()
        return render_template("material/cadastrar.html", erro=str(e), categorias=categorias)

@material_bp.route("/<int:id>/editar", methods=["GET", "POST"])
def editar(id):
    if request.method == "GET":
        material = Material.query.get(id)
        # <-- ADICIONADO: Busca as categorias para o HTML montar a caixinha
        categorias = Categoria.query.all()
        return render_template("material/editar.html", material=material, categorias=categorias)

    conteudo = request.form.get("conteudo")
    url = request.form.get("url")
    categoria_id = request.form.get("categoria_id")
    
    service = EditarMaterialService()
    try:
        service.executar(id, conteudo, url, categoria_id)
        return redirect(url_for("material.listar"))
    except ValueError as e:
        material = Material.query.get(id)
        categorias = Categoria.query.all()
        return render_template("material/editar.html", material=material, categorias=categorias, erro=str(e))

@material_bp.route("/<int:id>/deletar", methods=["POST"])
def deletar(id):
    service = DeletarMaterialService()
    service.executar(id)
    return redirect(url_for("material.listar"))