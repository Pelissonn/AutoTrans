from flask import Blueprint, render_template, request, redirect, url_for
from models import Categoria
from services.categorias.create_categoria_service import CadastrarCategoriaService
from services.categorias.read_categoria_service import ListarCategoriasService
from services.categorias.update_categoria_service import EditarCategoriaService
from services.categorias.delete_categoria_service import DeletarCategoriaService

categoria_bp = Blueprint('categoria', __name__,url_prefix="/categorias")

@categoria_bp.route("/")
def listar():   
    service = ListarCategoriasService()
    categorias = service.executar()
    lista = [{"id": c.id, "nome": c.nome, "descricao": c.descricao} for c in categorias]
    return render_template("categoria/listar.html", categorias=categorias)

@categoria_bp.route("/cadastrar", methods=["GET", "POST"])
def cadastrar():
    if request.method == "GET":
        return render_template("categoria/cadastrar.html")
    nome = request.form.get("nome")
    descricao = request.form.get("descricao")
    service = CadastrarCategoriaService()
    try:
        service.executar(nome, descricao)
        # Se deu certo, manda de volta para a lista de categorias
        return redirect(url_for("categoria.listar"))
    except ValueError as e:
        # Se deu erro no Service, mostra a tela de cadastro de novo com a mensagem de erro
        return render_template("categoria/cadastrar.html", erro=str(e))

@categoria_bp.route("/<int:id>/editar", methods=["GET", "POST"])
def editar(id):
    if request.method == "GET":
        # Vai ao banco de dados procurar a categoria para preencher o formulário
        categoria = Categoria.query.get(id)
        return render_template("categoria/editar.html", categoria=categoria)

    nome = request.form.get("nome")
    descricao = request.form.get("descricao")
    service = EditarCategoriaService()
    
    try:
        service.executar(id, nome, descricao)
        # Se deu certo, volta para a lista
        return redirect(url_for("categoria.listar"))
    except ValueError as e:
        categoria = Categoria.query.get(id)
        return render_template("categoria/editar.html", categoria=categoria, erro=str(e))

@categoria_bp.route("/<int:id>/deletar", methods=["POST"])
def deletar(id):
    service = DeletarCategoriaService()
    service.executar(id)
    # Apaga e volta à lista de imediato
    return redirect(url_for("categoria.listar"))
