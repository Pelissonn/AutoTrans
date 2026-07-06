from models import db, Questao

class DeletarQuestaoService:
    def executar(self, questao_id):
        questao = Questao.query.get(questao_id)
        if not questao:
            raise ValueError("Questão não encontrada.")
        db.session.delete(questao)
        db.session.commit()