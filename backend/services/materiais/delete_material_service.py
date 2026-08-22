from models import Material


class DeletarMaterialService:
    def executar(self, material_id):
        material = Material.buscar_por_id(material_id)
        if material is None:
            raise ValueError("Material não encontrado.")

        material.deletar()
        return True
