from flask import Blueprint, request

from controllers.base_controller import ERROS_DE_NEGOCIO, BaseController
from services.auth import LoginService, RegistrarUsuarioService
from services.usuarios import BuscarUsuarioService, EditarUsuarioService, ExcluirUsuarioService
from utils.auth import gerar_token, login_obrigatorio

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


class RegistroController(BaseController):
    """Criar conta: POST /auth/registro {nome, email, senha, aceitou_termos}."""

    def post(self):
        dados = self.dados_json()
        try:
            usuario = RegistrarUsuarioService().executar(
                nome=dados.get("nome"),
                email=dados.get("email"),
                senha=dados.get("senha"),
                aceitou_termos=dados.get("aceitou_termos"),
            )
            return self.responder({"token": gerar_token(usuario.id), "usuario": usuario.to_dict()}, 201)
        except ERROS_DE_NEGOCIO as erro:
            return self.responder_erro(erro)


class LoginController(BaseController):
    """Login: POST /auth/login {email, senha}."""

    def post(self):
        dados = self.dados_json()
        try:
            usuario = LoginService().executar(dados.get("email"), dados.get("senha"))
            return self.responder({"token": gerar_token(usuario.id), "usuario": usuario.to_dict()})
        except ValueError as erro:
            return self.responder({"erro": str(erro)}, 401)


class LogoutController(BaseController):
    """Logout: o token é descartado pelo frontend; a rota existe por simetria da API."""

    def post(self):
        return self.responder({"mensagem": "Sessão encerrada."})


class PerfilController(BaseController):
    """
    /auth/me — a própria conta do usuário logado. O id vem SEMPRE do token,
    nunca da URL ou do corpo: ninguém mexe na conta de outra pessoa.
    """

    decorators = [login_obrigatorio]

    def get(self):
        try:
            return self.responder(BuscarUsuarioService().executar(request.usuario_id))
        except ERROS_DE_NEGOCIO as erro:
            return self.responder_erro(erro)

    def put(self):
        dados = self.dados_json()
        try:
            # is_admin nunca vem daqui: ninguém se autopromove a administrador.
            usuario = EditarUsuarioService().executar(
                request.usuario_id,
                nome=dados.get("nome"),
                email=dados.get("email"),
                senha=dados.get("senha"),
                foto_url=dados.get("foto_url"),
            )
            return self.responder(usuario)
        except ERROS_DE_NEGOCIO as erro:
            return self.responder_erro(erro)

    def delete(self):
        try:
            return self.responder(ExcluirUsuarioService().executar(request.usuario_id))
        except ERROS_DE_NEGOCIO as erro:
            return self.responder_erro(erro)


auth_bp.add_url_rule("/registro", view_func=RegistroController.as_view("registro"), methods=["POST"])
auth_bp.add_url_rule("/login", view_func=LoginController.as_view("login"), methods=["POST"])
auth_bp.add_url_rule("/logout", view_func=LogoutController.as_view("logout"), methods=["POST"])
auth_bp.add_url_rule("/me", view_func=PerfilController.as_view("perfil"), methods=["GET", "PUT", "DELETE"])
