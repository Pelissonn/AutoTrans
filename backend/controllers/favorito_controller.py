from flask import Blueprint, request

from controllers.base_controller import ERROS_DE_NEGOCIO, BaseController
from services.favoritos import FavoritarQuestaoService, ListarFavoritosService, RemoverFavoritoService
from utils.auth import login_obrigatorio

favorito_bp = Blueprint("favorito", __name__, url_prefix="/favoritos")


class FavoritoController(BaseController):
    """Questões favoritas do aluno logado (o usuário vem do token)."""

    decorators = [login_obrigatorio]

    def get(self):
        return self.responder(ListarFavoritosService().executar(request.usuario_id))

    def post(self):
        dados = self.dados_json()
        try:
            favorito = FavoritarQuestaoService().executar(request.usuario_id, dados.get("questao_id"))
            return self.responder(favorito, 201)
        except ERROS_DE_NEGOCIO as erro:
            return self.responder_erro(erro)

    def delete(self, questao_id):
        try:
            return self.responder(RemoverFavoritoService().executar(request.usuario_id, questao_id))
        except ERROS_DE_NEGOCIO as erro:
            return self.responder_erro(erro)


favorito_view = FavoritoController.as_view("favorito_api")
favorito_bp.add_url_rule("/", view_func=favorito_view, methods=["GET", "POST"])
favorito_bp.add_url_rule("/<int:questao_id>", view_func=favorito_view, methods=["DELETE"])
