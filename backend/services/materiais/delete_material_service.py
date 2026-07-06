from models import db, Material

class DeletarMaterialService:
    def executar(self, material_id):
        material = Material.query.get(material_id)
        if not material:
            raise ValueError("Material não encontrado.")
        db.session.delete(material)
        db.session.commit()