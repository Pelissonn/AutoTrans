from models import db, Questao, Categoria
class EditarQuestaoService:
    def executar(self, questao_id, enunciado=None, categoria_id=None):
        questao = Questao.query.get(questao_id)
        if not questao:
            raise ValueError("Questão não encontrada.")
        
        if enunciado is not None:
            questao.enunciado = enunciado
        
        if categoria_id is not None:
            categoria = Categoria.query.get(categoria_id)
            if not categoria:
                raise ValueError("Categoria não encontrada.")
            questao.categoria_id = categoria_id
        
        db.session.commit()