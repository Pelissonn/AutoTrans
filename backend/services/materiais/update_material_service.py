from models import Material


class EditarMaterialService:
    def executar(self, material_id, conteudo, url):
        material = Material.buscar_por_id(material_id)
        if material is None:
            raise ValueError("Material não encontrado.")

        if not conteudo:
            raise ValueError("O conteúdo é obrigatório.")

        material.atualizar(conteudo=conteudo, url=url)
        return material.to_dict()
