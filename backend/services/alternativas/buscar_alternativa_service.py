from models import Alternativa
from services.excecoes import RecursoNaoEncontrado


class BuscarAlternativaService:
    """Caso de uso: consultar uma alternativa pelo id."""

    def executar(self, alternativa_id):
        alternativa = Alternativa.buscar_por_id(alternativa_id)
        if alternativa is None:
            raise RecursoNaoEncontrado("Alternativa não encontrada.")
        return alternativa.to_dict()
