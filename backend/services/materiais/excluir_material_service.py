from models import Material
from services.excecoes import RecursoNaoEncontrado


class ExcluirMaterialService:
    """Caso de uso: excluir um material de estudo."""

    def executar(self, material_id):
        material = Material.buscar_por_id(material_id)
        if material is None:
            raise RecursoNaoEncontrado("Material não encontrado.")

        material.deletar()
        return {"mensagem": "Material excluído com sucesso."}
