from models import db, Material, Categoria

class EditarMaterialService:
    def executar(self, material_id, conteudo=None, url=None, categoria_id=None):
        material = Material.query.get(material_id)
        if not material:
            raise ValueError("Material não encontrado.")
        
        if conteudo:
            material.conteudo = conteudo
        if url:
            material.url = url
        if categoria_id:
            categoria = Categoria.query.get(categoria_id)
            if not categoria:
                raise ValueError("Categoria não encontrada.")
            material.categoria = categoria
        
        db.session.commit()