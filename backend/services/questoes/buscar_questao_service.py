from models import Questao
from services.excecoes import RecursoNaoEncontrado


class BuscarQuestaoService:
    """Caso de uso: consultar uma questão pelo id."""

    def executar(self, questao_id):
        questao = Questao.buscar_por_id(questao_id)
        if questao is None:
            raise RecursoNaoEncontrado("Questão não encontrada.")
        return questao.to_dict()
