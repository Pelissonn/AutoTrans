from models import Questao


class ListarQuestoesService:
    def executar(self):
        questoes = Questao.listar_todos()
        return [questao.to_dict() for questao in questoes]


class BuscarQuestaoPorIdService:
    def executar(self, questao_id):
        questao = Questao.buscar_por_id(questao_id)
        if questao is None:
            return None
        return questao.to_dict()


class ListarQuestoesPorCategoriaService:
    def executar(self, categoria_id):
        questoes = Questao.listar_por_categoria(categoria_id)
        return [questao.to_dict() for questao in questoes]
