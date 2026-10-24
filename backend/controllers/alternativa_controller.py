from flask import Blueprint, request

from controllers.base_controller import ERROS_DE_NEGOCIO, BaseController
from services.alternativas import (
    BuscarAlternativaService,
    CadastrarAlternativaService,
    EditarAlternativaService,
    ExcluirAlternativaService,
    ListarAlternativasPorQuestaoService,
    ListarAlternativasService,
)
from utils.auth import admin_obrigatorio

alternativa_bp = Blueprint("alternativa", __name__, url_prefix="/alternativas")


class AlternativaController(BaseController):
    """Alternativas: leitura pública (com filtro ?questao_id=), escrita só administrador."""

    def get(self, id=None):
        try:
            if id is not None:
                return self.responder(BuscarAlternativaService().executar(id))

            questao_id = request.args.get("questao_id", type=int)
            if questao_id:
                return self.responder(ListarAlternativasPorQuestaoService().executar(questao_id))
            return self.responder(ListarAlternativasService().executar())
        except ERROS_DE_NEGOCIO as erro:
            return self.responder_erro(erro)

    @admin_obrigatorio
    def post(self):
        dados = self.dados_json()
        try:
            alternativa = CadastrarAlternativaService().executar(
                dados.get("questao_id"), dados.get("texto"), dados.get("correta", False)
            )
            return self.responder(alternativa, 201)
        except ERROS_DE_NEGOCIO as erro:
            return self.responder_erro(erro)

    @admin_obrigatorio
    def put(self, id):
        dados = self.dados_json()
        try:
            alternativa = EditarAlternativaService().executar(id, dados.get("texto"), dados.get("correta"))
            return self.responder(alternativa)
        except ERROS_DE_NEGOCIO as erro:
            return self.responder_erro(erro)

    @admin_obrigatorio
    def delete(self, id):
        try:
            return self.responder(ExcluirAlternativaService().executar(id))
        except ERROS_DE_NEGOCIO as erro:
            return self.responder_erro(erro)


AlternativaController.registrar_crud(alternativa_bp, "alternativa_api")
