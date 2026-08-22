from models import Categoria, Questao


class EditarQuestaoService:
    def executar(self, questao_id, enunciado, categoria_id):
        questao = Questao.buscar_por_id(questao_id)
        if questao is None:
            raise ValueError("Questão não encontrada.")

        if not enunciado:
            raise ValueError("O enunciado é obrigatório.")

        if categoria_id and Categoria.buscar_por_id(categoria_id) is None:
            raise ValueError("Categoria não encontrada.")

        questao.atualizar(enunciado=enunciado, categoria_id=categoria_id)
        return questao.to_dict()
