from models import db, Material, Categoria

class CadastrarMaterialService:
    def executar(self, conteudo, url, categoria_id):
        if not conteudo:
            raise ValueError("O conteúdo do material é obrigatório.")
        if not url:
            raise ValueError("A URL do material é obrigatória.")

        categoria = Categoria.query.get(categoria_id)
        if not categoria:
            raise ValueError("Categoria não encontrada.")

        material = Material(conteudo=conteudo, url=url, categoria=categoria)
        db.session.add(material)
        db.session.commit()
    