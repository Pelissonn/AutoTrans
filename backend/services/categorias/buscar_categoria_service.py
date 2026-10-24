from models import Categoria
from services.excecoes import RecursoNaoEncontrado


class BuscarCategoriaService:
    """Caso de uso: consultar uma categoria pelo id."""

    def executar(self, categoria_id):
        categoria = Categoria.buscar_por_id(categoria_id)
        if categoria is None:
            raise RecursoNaoEncontrado("Categoria não encontrada.")
        return categoria.to_dict()
