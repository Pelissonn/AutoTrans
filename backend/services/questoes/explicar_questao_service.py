from models import Alternativa, Questao
from services.excecoes import RecursoNaoEncontrado
from services.ia.gemini_service import GeminiService


class ExplicarQuestaoService:
    """
    Caso de uso: o aluno pede para a IA explicar por que a alternativa
    correta está certa (e, se ele errou, por que a dele está errada).

    Este Service monta o pedido; a comunicação com a API do Gemini fica
    encapsulada no GeminiService.
    """

    def __init__(self, ia=None):
        self.ia = ia or GeminiService()

    def executar(self, questao_id, alternativa_escolhida_id=None):
        questao = Questao.buscar_por_id(questao_id)
        if questao is None:
            raise RecursoNaoEncontrado("Questão não encontrada.")

        correta = questao.alternativa_correta()
        if correta is None:
            raise ValueError("Esta questão ainda não tem alternativa correta cadastrada.")

        escolhida = None
        if alternativa_escolhida_id:
            escolhida = Alternativa.buscar_por_id(alternativa_escolhida_id)
            if escolhida is None or escolhida.questao_id != questao.id:
                raise ValueError("A alternativa informada não pertence a esta questão.")

        explicacao = self.ia.gerar_texto(self._montar_prompt(questao, correta, escolhida))

        return {
            "questao_id": questao.id,
            "alternativa_correta_id": correta.id,
            "explicacao": explicacao,
        }

    def _montar_prompt(self, questao, correta, escolhida):
        alternativas = "\n".join(f"- {a.texto}" for a in questao.alternativas)
        prompt = (
            "Você é um instrutor de autoescola no Brasil. Explique de forma curta "
            "(no máximo 5 frases), clara, em texto simples sem markdown, e baseada no Código de Trânsito Brasileiro "
            "a questão da prova teórica da CNH abaixo.\n\n"
            f"Categoria: {questao.categoria.nome}\n"
            f"Questão: {questao.enunciado}\n"
            f"Alternativas:\n{alternativas}\n"
            f"Alternativa correta: {correta.texto}\n"
        )
        if escolhida is not None and escolhida.id != correta.id:
            prompt += f"O aluno marcou: {escolhida.texto}. Explique também por que essa está errada.\n"
        return prompt
