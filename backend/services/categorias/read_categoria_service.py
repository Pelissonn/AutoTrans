from models import Categoria

class ListarCategoriasService:
    def executar(self):
        return Categoria.query.all()