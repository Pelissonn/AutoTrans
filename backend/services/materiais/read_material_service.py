from models import Material


class ListarMateriaisService:
    def executar(self):
        materiais = Material.listar_todos()
        return [material.to_dict() for material in materiais]


class BuscarMaterialPorIdService:
    def executar(self, material_id):
        material = Material.buscar_por_id(material_id)
        if material is None:
            return None
        return material.to_dict()


class ListarMateriaisPorCategoriaService:
    def executar(self, categoria_id):
        materiais = Material.listar_por_categoria(categoria_id)
        return [material.to_dict() for material in materiais]
