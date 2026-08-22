from models import Alternativa


class DeletarAlternativaService:
    def executar(self, alternativa_id):
        alternativa = Alternativa.buscar_por_id(alternativa_id)
        if alternativa is None:
            raise ValueError("Alternativa não encontrada.")

        alternativa.deletar()
        return True
