from models import Alternativa


class ListarAlternativasService:
    def executar(self):
        alternativas = Alternativa.listar_todos()
        return [alternativa.to_dict() for alternativa in alternativas]


class BuscarAlternativaPorIdService:
    def executar(self, alternativa_id):
        alternativa = Alternativa.buscar_por_id(alternativa_id)
        if alternativa is None:
            return None
        return alternativa.to_dict()


class ListarAlternativasPorQuestaoService:
    def executar(self, questao_id):
        alternativas = Alternativa.listar_por_questao(questao_id)
        return [alternativa.to_dict() for alternativa in alternativas]
