from flask import Blueprint, request

from controllers.base_controller import ERROS_DE_NEGOCIO, BaseController
from services.questoes import (
    BuscarQuestaoService,
    BuscarQuestoesPorPalavraService,
    CadastrarQuestaoService,
    EditarQuestaoService,
    ExcluirQuestaoService,
    ExplicarQuestaoService,
    ImportarQuestoesService,
    ListarQuestoesErradasService,
    ListarQuestoesPorCategoriaService,
    ListarQuestoesService,
)
from utils.auth import admin_obrigatorio, login_obrigatorio

questao_bp = Blueprint("questao", __name__, url_prefix="/questoes")


class QuestaoController(BaseController):
    """Questões: leitura pública (com filtro ?categoria_id=), escrita só administrador."""

    def get(self, id=None):
        try:
            if id is not None:
                return self.responder(BuscarQuestaoService().executar(id))

            categoria_id = request.args.get("categoria_id", type=int)
            if categoria_id:
                return self.responder(ListarQuestoesPorCategoriaService().executar(categoria_id))
            return self.responder(ListarQuestoesService().executar())
        except ERROS_DE_NEGOCIO as erro:
            return self.responder_erro(erro)

    @admin_obrigatorio
    def post(self):
        dados = self.dados_json()
        try:
            questao = CadastrarQuestaoService().executar(dados.get("enunciado"), dados.get("categoria_id"))
            return self.responder(questao, 201)
        except ERROS_DE_NEGOCIO as erro:
            return self.responder_erro(erro)

    @admin_obrigatorio
    def put(self, id):
        dados = self.dados_json()
        try:
            questao = EditarQuestaoService().executar(id, dados.get("enunciado"), dados.get("categoria_id"))
            return self.responder(questao)
        except ERROS_DE_NEGOCIO as erro:
            return self.responder_erro(erro)

    @admin_obrigatorio
    def delete(self, id):
        try:
            return self.responder(ExcluirQuestaoService().executar(id))
        except ERROS_DE_NEGOCIO as erro:
            return self.responder_erro(erro)


class BuscaQuestaoController(BaseController):
    """GET /questoes/buscar?q=palavra[&categoria_id=] — busca por palavra-chave."""

    def get(self):
        try:
            questoes = BuscarQuestoesPorPalavraService().executar(
                request.args.get("q"), request.args.get("categoria_id", type=int)
            )
            return self.responder(questoes)
        except ERROS_DE_NEGOCIO as erro:
            return self.responder_erro(erro)


class CadernoErrosController(BaseController):
    """GET /questoes/erradas — caderno de erros do aluno logado."""

    decorators = [login_obrigatorio]

    def get(self):
        return self.responder(ListarQuestoesErradasService().executar(request.usuario_id))


class ImportacaoQuestoesController(BaseController):
    """POST /questoes/importar — importação em lote por arquivo JSON (administrador)."""

    decorators = [admin_obrigatorio]

    def post(self):
        dados = request.get_json(silent=True)
        if dados is None:
            return self.responder({"erro": "Envie um JSON válido no corpo da requisição."}, 400)
        try:
            return self.responder(ImportarQuestoesService().executar(dados), 201)
        except ERROS_DE_NEGOCIO as erro:
            return self.responder_erro(erro)


class ExplicacaoQuestaoController(BaseController):
    """POST /questoes/<id>/explicacao {alternativa_escolhida_id?} — explicação gerada por IA."""

    decorators = [login_obrigatorio]

    def post(self, id):
        dados = self.dados_json()
        try:
            explicacao = ExplicarQuestaoService().executar(id, dados.get("alternativa_escolhida_id"))
            return self.responder(explicacao)
        except ERROS_DE_NEGOCIO as erro:
            return self.responder_erro(erro)


QuestaoController.registrar_crud(questao_bp, "questao_api")
questao_bp.add_url_rule("/buscar", view_func=BuscaQuestaoController.as_view("questao_busca"), methods=["GET"])
questao_bp.add_url_rule("/erradas", view_func=CadernoErrosController.as_view("questao_erradas"), methods=["GET"])
questao_bp.add_url_rule(
    "/importar", view_func=ImportacaoQuestoesController.as_view("questao_importar"), methods=["POST"]
)
questao_bp.add_url_rule(
    "/<int:id>/explicacao",
    view_func=ExplicacaoQuestaoController.as_view("questao_explicacao"),
    methods=["POST"],
)
