from flask import Blueprint

from controllers.base_controller import ERROS_DE_NEGOCIO, BaseController
from services.usuarios import (
    BuscarUsuarioService,
    CadastrarUsuarioService,
    EditarUsuarioService,
    ExcluirUsuarioService,
    ListarUsuariosService,
)
from utils.auth import admin_obrigatorio

usuario_bp = Blueprint("usuario", __name__, url_prefix="/usuarios")


class UsuarioController(BaseController):
    """Gestão de usuários (somente administrador)."""

    decorators = [admin_obrigatorio]

    def get(self, id=None):
        if id is None:
            return self.responder(ListarUsuariosService().executar())
        try:
            return self.responder(BuscarUsuarioService().executar(id))
        except ERROS_DE_NEGOCIO as erro:
            return self.responder_erro(erro)

    def post(self):
        dados = self.dados_json()
        try:
            usuario = CadastrarUsuarioService().executar(
                dados.get("nome"), dados.get("email"), dados.get("senha"), dados.get("is_admin", False)
            )
            return self.responder(usuario, 201)
        except ERROS_DE_NEGOCIO as erro:
            return self.responder_erro(erro)

    def put(self, id):
        dados = self.dados_json()
        try:
            usuario = EditarUsuarioService().executar(
                id,
                nome=dados.get("nome"),
                email=dados.get("email"),
                senha=dados.get("senha"),
                foto_url=dados.get("foto_url"),
                is_admin=dados.get("is_admin"),
            )
            return self.responder(usuario)
        except ERROS_DE_NEGOCIO as erro:
            return self.responder_erro(erro)

    def delete(self, id):
        try:
            return self.responder(ExcluirUsuarioService().executar(id))
        except ERROS_DE_NEGOCIO as erro:
            return self.responder_erro(erro)


UsuarioController.registrar_crud(usuario_bp, "usuario_api")
