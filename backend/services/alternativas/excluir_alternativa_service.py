from models import Alternativa
from repositories import AlternativaRepository
from services.excecoes import RecursoNaoEncontrado


class ExcluirAlternativaService:
    """Caso de uso: excluir uma alternativa (bloqueado se já foi escolhida em simulado)."""

    def __init__(self):
        self.repositorio = AlternativaRepository()

    def executar(self, alternativa_id):
        alternativa = Alternativa.buscar_por_id(alternativa_id)
        if alternativa is None:
            raise RecursoNaoEncontrado("Alternativa não encontrada.")

        total = self.repositorio.contar_respostas(alternativa_id)
        if total > 0:
            raise ValueError(
                f"Não é possível excluir: esta alternativa já foi escolhida em {total} simulado(s)."
            )

        alternativa.deletar()
        return {"mensagem": "Alternativa excluída com sucesso."}
