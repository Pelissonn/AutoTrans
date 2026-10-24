from models import Material
from services.excecoes import RecursoNaoEncontrado


class BuscarMaterialService:
    """Caso de uso: consultar um material pelo id."""

    def executar(self, material_id):
        material = Material.buscar_por_id(material_id)
        if material is None:
            raise RecursoNaoEncontrado("Material não encontrado.")
        return material.to_dict()
