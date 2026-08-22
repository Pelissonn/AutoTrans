from models import Alternativa, Questao


class CadastrarAlternativaService:
    def executar(self, questao_id, texto, correta=False):
        if not texto:
            raise ValueError("O texto da alternativa é obrigatório.")

        questao = Questao.buscar_por_id(questao_id)
        if questao is None:
            raise ValueError("Questão não encontrada.")

        alternativa = Alternativa(questao_id=questao_id, texto=texto, correta=bool(correta))
        alternativa.salvar()
        return alternativa.to_dict()
