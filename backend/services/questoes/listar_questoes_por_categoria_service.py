from models import Categoria
from repositories import QuestaoRepository
from services.excecoes import RecursoNaoEncontrado
from services.questoes.formatador_questao import anexar_alternativas


class ListarQuestoesPorCategoriaService:
    """Caso de uso: filtrar as questões de uma categoria."""

    def __init__(self):
        self.repositorio = QuestaoRepository()

    def executar(self, categoria_id):
        if Categoria.buscar_por_id(categoria_id) is None:
            raise RecursoNaoEncontrado("Categoria não encontrada.")

        return anexar_alternativas(self.repositorio.listar_por_categoria(categoria_id))
