from models import Categoria, Questao


class CadastrarQuestaoService:
    def executar(self, enunciado, categoria_id):
        if not enunciado:
            raise ValueError("O enunciado da questão é obrigatório.")

        categoria = Categoria.buscar_por_id(categoria_id)
        if categoria is None:
            raise ValueError("Categoria não encontrada.")

        questao = Questao(enunciado=enunciado, categoria_id=categoria_id)
        questao.salvar()
        return questao.to_dict()
