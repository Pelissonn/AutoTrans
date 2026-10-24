from models import Questao
from repositories import QuestaoRepository
from services.excecoes import RecursoNaoEncontrado


class ExcluirQuestaoService:
    """
    Caso de uso: excluir uma questão (as alternativas saem junto).
    Bloqueado se a questão já foi respondida em algum simulado.
    """

    def __init__(self):
        self.repositorio = QuestaoRepository()

    def executar(self, questao_id):
        questao = Questao.buscar_por_id(questao_id)
        if questao is None:
            raise RecursoNaoEncontrado("Questão não encontrada.")

        total = self.repositorio.contar_respostas_em_simulados(questao_id)
        if total > 0:
            raise ValueError(
                f"Não é possível excluir: a questão já apareceu em {total} simulado(s) "
                "de alunos. Excluí-la apagaria parte do histórico deles."
            )

        questao.deletar()
        return {"mensagem": "Questão excluída com sucesso."}
