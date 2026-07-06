from flask import Blueprint, render_template, request, redirect, url_for
from models import Alternativa, Questao
from services.alternativas.create_alternativa_service import CadastrarAlternativaService
from services.alternativas.read_alternativa_service import ListarAlternativasService
from services.alternativas.update_alternativa_service import AtualizarAlternativaService
from services.alternativas.delete_alternativa_service import DeletarAlternativaService

alternativa_bp = Blueprint('alternativa', __name__, url_prefix="/alternativas")

@alternativa_bp.route("/")
def listar():
    service = ListarAlternativasService()
    alternativas = service.executar()
    return render_template("alternativa/listar.html", alternativas=alternativas)

@alternativa_bp.route("/cadastrar", methods=["GET", "POST"])
def cadastrar():
    if request.method == "GET":
        questoes = Questao.query.all()
        return render_template("alternativa/cadastrar.html", questoes=questoes)
    
    texto = request.form.get("texto")
    correta = request.form.get("correta") == "true"
    questao_id = request.form.get("questao_id")
    
    service = CadastrarAlternativaService()
    try:
        service.executar(texto, correta, questao_id)
        return redirect(url_for("alternativa.listar"))
    except ValueError as e:
        questoes = Questao.query.all()
        return render_template("alternativa/cadastrar.html", erro=str(e), questoes=questoes)
    
@alternativa_bp.route("/<int:id>/editar", methods=["GET", "POST"])
def editar(id):
    if request.method == "GET":
        alternativa = Alternativa.query.get(id)
        questoes = Questao.query.all()
        return render_template("alternativa/editar.html", alternativa=alternativa, questoes=questoes)

    texto = request.form.get("texto")
    correta = request.form.get("correta") == "true"
    questao_id = request.form.get("questao_id")
    
    service = AtualizarAlternativaService()
    try:
        service.executar(id, texto, correta, questao_id)
        return redirect(url_for("alternativa.listar"))
    except ValueError as e:
        alternativa = Alternativa.query.get(id)
        questoes = Questao.query.all()
        return render_template("alternativa/editar.html", alternativa=alternativa, questoes=questoes, erro=str(e))
    
@alternativa_bp.route("/<int:id>/deletar", methods=["POST"])
def deletar(id):
    service = DeletarAlternativaService()
    service.executar(id)
    return redirect(url_for("alternativa.listar"))