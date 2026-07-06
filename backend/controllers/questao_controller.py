from flask import Blueprint, render_template, request, redirect, url_for
from models import Questao, Categoria
from services.questoes.create_questao_service import CadastrarQuestaoService
from services.questoes.read_questao_service import ListarQuestoesService
from services.questoes.update_questao_service import EditarQuestaoService
from services.questoes.delete_questao_service import DeletarQuestaoService

questao_bp = Blueprint('questao', __name__,url_prefix="/questoes")

@questao_bp.route("/")
def listar():
    service = ListarQuestoesService()
    questoes = service.executar()
    return render_template("questao/listar.html", questoes=questoes)

@questao_bp.route("/cadastrar", methods=["GET", "POST"])
def cadastrar():
    if request.method == "GET":
        categorias = Categoria.query.all() 
        return render_template("questao/cadastrar.html", categorias=categorias)
    
    enunciado = request.form.get("enunciado")
    categoria_id = request.form.get("categoria_id")
    
    service = CadastrarQuestaoService()
    try:
        service.executar(enunciado, categoria_id)
        return redirect(url_for("questao.listar"))
    except ValueError as e:
        categorias = Categoria.query.all()
        return render_template("questao/cadastrar.html", erro=str(e), categorias=categorias)

@questao_bp.route("/<int:id>/editar", methods=["GET", "POST"])
def editar(id):
    if request.method == "GET":
        questao = Questao.query.get(id)
        categorias = Categoria.query.all()
        return render_template("questao/editar.html", questao=questao, categorias=categorias)

    enunciado = request.form.get("enunciado")
    categoria_id = request.form.get("categoria_id")
    
    service = EditarQuestaoService()
    try:
        service.executar(id, enunciado, categoria_id)
        return redirect(url_for("questao.listar"))
    except ValueError as e:
        questao = Questao.query.get(id)
        categorias = Categoria.query.all()
        return render_template("questao/editar.html", questao=questao, categorias=categorias, erro=str(e))
    
@questao_bp.route("/<int:id>/deletar", methods=["POST"])
def deletar(id):
    service = DeletarQuestaoService()
    service.executar(id)
    return redirect(url_for("questao.listar"))

