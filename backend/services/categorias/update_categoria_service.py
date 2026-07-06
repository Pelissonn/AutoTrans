from models import db, Categoria

class EditarCategoriaService:
    def executar(self, categoria_id, nome, descricao):
        categoria = Categoria.query.get(categoria_id)
        if not categoria:
            raise ValueError("Categoria não encontrada.")
            
        if not nome or not descricao:
            raise ValueError("Nome e descrição são obrigatórios!")
        
        categoria.nome = nome
        categoria.descricao = descricao
        db.session.commit()