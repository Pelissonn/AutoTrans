from models import Categoria


class ListarCategoriasService:
    """Caso de uso: listar as categorias (trilhas) de estudo."""

    def executar(self):
        return [categoria.to_dict() for categoria in Categoria.listar_todos()]
