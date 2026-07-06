from models import Alternativa


class ListarAlternativasService:
    def executar(self):
        return Alternativa.query.all()