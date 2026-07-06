from models import db, Questao, Categoria

class CadastrarQuestaoService:
    def executar(self, enunciado, categoria_id):
        if not enunciado:
            raise ValueError("O enunciado da questão é obrigatório.")
        
        categoria = Categoria.query.get(categoria_id)
        if not categoria:
            raise ValueError("Categoria não encontrada.")
        
        questao = Questao(enunciado=enunciado, categoria_id=categoria_id)
        db.session.add(questao)
        db.session.commit()
    