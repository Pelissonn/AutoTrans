from models import Categoria, Questao
from services.excecoes import RecursoNaoEncontrado


class EditarQuestaoService:
    """Caso de uso: editar o enunciado ou a categoria de uma questão."""

    def executar(self, questao_id, enunciado, categoria_id=None):
        questao = Questao.buscar_por_id(questao_id)
        if questao is None:
            raise RecursoNaoEncontrado("Questão não encontrada.")

        enunciado = (enunciado or "").strip()
        if not enunciado:
            raise ValueError("O enunciado da questão é obrigatório.")

        if categoria_id and Categoria.buscar_por_id(categoria_id) is None:
            raise RecursoNaoEncontrado("Categoria não encontrada.")

        questao.atualizar(enunciado=enunciado, categoria_id=categoria_id)
        return questao.to_dict()
