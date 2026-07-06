from models import Material

class ListarMateriaisService:
    def executar(self):
        return Material.query.all()
    