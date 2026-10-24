from repositories import QuestaoRepository
from services.questoes.formatador_questao import anexar_alternativas


class BuscarQuestoesPorPalavraService:
    """Caso de uso: o aluno procura questões por uma palavra-chave."""

    def __init__(self):
        self.repositorio = QuestaoRepository()

    def executar(self, palavra, categoria_id=None):
        palavra = (palavra or "").strip()
        if len(palavra) < 2:
            raise ValueError("Digite pelo menos 2 letras para buscar.")

        linhas = self.repositorio.buscar_por_palavra(palavra, categoria_id)
        return anexar_alternativas(linhas)
