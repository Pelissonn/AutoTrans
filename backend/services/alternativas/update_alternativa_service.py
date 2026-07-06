from models import db, Alternativa, Questao

class AtualizarAlternativaService:
    def executar(self, alternativa_id, questao_id, texto, correta):
        alternativa = Alternativa.query.get(alternativa_id)
        if not alternativa:
            raise ValueError("Alternativa não encontrada.")

        if not questao_id:
            raise ValueError("O ID da questão é obrigatório.")
        if not texto:
            raise ValueError("O texto da alternativa é obrigatório.")
        if correta not in [True, False]:
            raise ValueError("O valor de 'correta' deve ser True ou False.")

        questao = Questao.query.get(questao_id)
        if not questao:
            raise ValueError("Questão não encontrada.")

        alternativa.questao_id = questao_id
        alternativa.texto = texto
        alternativa.correta = correta
        db.session.commit()