from flask import Blueprint, render_template, request, redirect, url_for
from models import Usuario
from services.usuario.create_usuario_service import CadastrarUsuarioService
from services.usuario.read_usuarios_service import ListarUsuariosService
from services.usuario.update_usuario_serivce import EditarUsuarioService
from services.usuario.delete_usuario_service import DeletarUsuarioService

usuario_bp = Blueprint('usuario', __name__,url_prefix="/usuarios")

@usuario_bp.route("/")
def listar():
    service = ListarUsuariosService()
    usuarios = service.executar()
    lista = [{"id": u.id, "nome": u.nome, "email": u.email} for u in usuarios]
    return render_template("usuario/listar.html", usuarios=usuarios)

@usuario_bp.route("/cadastrar", methods=["GET", "POST"])
def cadastrar():
    if request.method == "GET":
        return render_template("usuario/cadastrar.html")
    nome = request.form.get("nome")
    email = request.form.get("email")
    service = CadastrarUsuarioService()
    try:
        service.executar(nome, email)
        # Se deu certo, manda de volta para a lista de usuários
        return redirect(url_for("usuario.listar"))
    except ValueError as e:
        # Se deu erro no Service, mostra a tela de cadastro de novo com a mensagem de erro
        return render_template("usuario/cadastrar.html", erro=str(e))

@usuario_bp.route("/<int:id>/editar", methods=["GET", "POST"])
def editar(id):
    if request.method == "GET":
        # Vai ao banco de dados procurar o utilizador para preencher o formulário
        usuario = Usuario.query.get(id)
        return render_template("usuario/editar.html", usuario=usuario)

    nome = request.form.get("nome")
    email = request.form.get("email")
    service = EditarUsuarioService()
    
    try:
        service.executar(id, nome, email)
        # Se deu certo, volta para a lista
        return redirect(url_for("usuario.listar"))
    except ValueError as e:
        usuario = Usuario.query.get(id)
        return render_template("usuario/editar.html", usuario=usuario, erro=str(e))


@usuario_bp.route("/<int:id>/deletar", methods=["POST"])
def deletar(id):
    service = DeletarUsuarioService()
    service.executar(id)
    # Apaga e volta à lista de imediato
    return redirect(url_for("usuario.listar"))