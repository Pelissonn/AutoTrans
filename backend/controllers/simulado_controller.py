from flask import Blueprint, request

from controllers.base_controller import ERROS_DE_NEGOCIO, BaseController
from services.simulados import (
    BuscarSimuladoService,
    ConsultarGabaritoService,
    ConsultarHistoricoService,
    FinalizarSimuladoService,
    IniciarSimuladoService,
)
from utils.auth import login_obrigatorio

simulado_bp = Blueprint("simulado", __name__, url_prefix="/simulados")


class SimuladoController(BaseController):
    """Iniciar um simulado e ver seus detalhes (o usuário sempre vem do token)."""

    decorators = [login_obrigatorio]

    def get(self, id):
        try:
            return self.responder(BuscarSimuladoService().executar(id, request.usuario_id))
        except ERROS_DE_NEGOCIO as erro:
            return self.responder_erro(erro)

    def post(self):
        dados = self.dados_json()
        try:
            simulado = IniciarSimuladoService().executar(request.usuario_id, dados.get("categoria_id"))
            return self.responder(simulado, 201)
        except ERROS_DE_NEGOCIO as erro:
            return self.responder_erro(erro)


class FinalizarSimuladoController(BaseController):
    """POST /simulados/<id>/finalizar {respostas: [{item_id, alternativa_id}]}."""

    decorators = [login_obrigatorio]

    def post(self, id):
        dados = self.dados_json()
        try:
            simulado = FinalizarSimuladoService().executar(id, dados.get("respostas", []), request.usuario_id)
            return self.responder(simulado)
        except ERROS_DE_NEGOCIO as erro:
            return self.responder_erro(erro)


class HistoricoSimuladoController(BaseController):
    """GET /simulados/historico — simulados finalizados e estatísticas do aluno."""

    decorators = [login_obrigatorio]

    def get(self):
        return self.responder(ConsultarHistoricoService().executar(request.usuario_id))


class GabaritoSimuladoController(BaseController):
    """GET /simulados/<id>/gabarito — correção questão a questão."""

    decorators = [login_obrigatorio]

    def get(self, id):
        try:
            return self.responder(ConsultarGabaritoService().executar(id, request.usuario_id))
        except ERROS_DE_NEGOCIO as erro:
            return self.responder_erro(erro)


simulado_view = SimuladoController.as_view("simulado_api")
simulado_bp.add_url_rule("/", view_func=simulado_view, methods=["POST"])
simulado_bp.add_url_rule("/<int:id>", view_func=simulado_view, methods=["GET"])
simulado_bp.add_url_rule(
    "/<int:id>/finalizar", view_func=FinalizarSimuladoController.as_view("simulado_finalizar"), methods=["POST"]
)
simulado_bp.add_url_rule(
    "/historico", view_func=HistoricoSimuladoController.as_view("simulado_historico"), methods=["GET"]
)
simulado_bp.add_url_rule(
    "/<int:id>/gabarito", view_func=GabaritoSimuladoController.as_view("simulado_gabarito"), methods=["GET"]
)
