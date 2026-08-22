from models import Categoria


class ListarCategoriasService:
    def executar(self):
        categorias = Categoria.listar_todos()
        return [categoria.to_dict() for categoria in categorias]


class BuscarCategoriaPorIdService:
    def executar(self, categoria_id):
        categoria = Categoria.buscar_por_id(categoria_id)
        if categoria is None:
            return None
        return categoria.to_dict()
