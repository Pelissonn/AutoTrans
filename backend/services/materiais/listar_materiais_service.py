from models import Material


class ListarMateriaisService:
    """Caso de uso: listar todos os materiais de estudo."""

    def executar(self):
        return [material.to_dict() for material in Material.listar_todos()]
