from models import Alternativa, db, Questao

class CadastrarAlternativaService:
    def executar(self, questao_id, texto, correta):
        if not questao_id:
            raise ValueError("O ID da questão é obrigatório.")
        if not texto:
            raise ValueError("O texto da alternativa é obrigatório.")
        if correta not in [True, False]:
            raise ValueError("O valor de 'correta' deve ser True ou False.")

        questao = Questao.query.get(questao_id)
        if not questao:
            raise ValueError("Questão não encontrada.")

        alternativa = Alternativa(questao_id=questao_id, texto=texto, correta=correta)
        db.session.add(alternativa)
        db.session.commit()