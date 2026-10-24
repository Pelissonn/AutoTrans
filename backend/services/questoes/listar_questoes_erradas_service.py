from repositories import QuestaoRepository
from services.questoes.formatador_questao import anexar_alternativas


class ListarQuestoesErradasService:
    """Caso de uso: caderno de erros — questões que o aluno mais errou."""

    def __init__(self):
        self.repositorio = QuestaoRepository()

    def executar(self, usuario_id):
        linhas = anexar_alternativas(self.repositorio.listar_erradas_por_usuario(usuario_id))

        return [
            {"total_erros": linha.pop("total_erros"), "questao": linha}
            for linha in linhas
        ]
