from models import Questao


class DeletarQuestaoService:
    def executar(self, questao_id):
        questao = Questao.buscar_por_id(questao_id)
        if questao is None:
            raise ValueError("Questão não encontrada.")

        questao.deletar()
        return True
