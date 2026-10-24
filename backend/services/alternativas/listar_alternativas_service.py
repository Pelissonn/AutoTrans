from models import Alternativa


class ListarAlternativasService:
    """Caso de uso: listar todas as alternativas cadastradas."""

    def executar(self):
        return [alternativa.to_dict() for alternativa in Alternativa.listar_todos()]
