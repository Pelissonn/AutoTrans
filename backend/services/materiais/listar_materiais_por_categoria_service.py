from models import Categoria
from repositories import MaterialRepository
from services.excecoes import RecursoNaoEncontrado


class ListarMateriaisPorCategoriaService:
    """Caso de uso: o aluno estuda os materiais de uma categoria."""

    def __init__(self):
        self.repositorio = MaterialRepository()

    def executar(self, categoria_id):
        if Categoria.buscar_por_id(categoria_id) is None:
            raise RecursoNaoEncontrado("Categoria não encontrada.")
        return self.repositorio.listar_por_categoria(categoria_id)
