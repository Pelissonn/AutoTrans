from models import Categoria, Questao
from services.excecoes import RecursoNaoEncontrado


class CadastrarQuestaoService:
    """Caso de uso: cadastrar uma questão em uma categoria."""

    def executar(self, enunciado, categoria_id):
        enunciado = (enunciado or "").strip()
        if not enunciado:
            raise ValueError("O enunciado da questão é obrigatório.")

        if Categoria.buscar_por_id(categoria_id) is None:
            raise RecursoNaoEncontrado("Categoria não encontrada.")

        questao = Questao(enunciado=enunciado, categoria_id=categoria_id)
        return questao.salvar().to_dict()
