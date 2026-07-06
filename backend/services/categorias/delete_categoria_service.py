from models import db, Categoria

class DeletarCategoriaService:
    def executar(self, categoria_id):
        categoria = Categoria.query.get(categoria_id)
        if not categoria:
            raise ValueError("Categoria não encontrada.")
        db.session.delete(categoria)
        db.session.commit()