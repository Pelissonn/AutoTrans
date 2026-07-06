from models import db, Categoria

class CadastrarCategoriaService:
    def executar(self, nome, descricao):
        if not nome:
            raise ValueError("O nome da categoria é obrigatório.")
        
        categoria = Categoria(nome=nome, descricao=descricao)
        db.session.add(categoria)
        db.session.commit()
    