from models import Questao
from repositories import AlternativaRepository
from services.excecoes import RecursoNaoEncontrado


class ListarAlternativasPorQuestaoService:
    """Caso de uso: filtrar as alternativas de uma questão."""

    def __init__(self):
        self.repositorio = AlternativaRepository()

    def executar(self, questao_id):
        if Questao.buscar_por_id(questao_id) is None:
            raise RecursoNaoEncontrado("Questão não encontrada.")
        return self.repositorio.listar_por_questao(questao_id)
