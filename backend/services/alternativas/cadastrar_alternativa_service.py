from models import Alternativa, Questao
from repositories import AlternativaRepository
from services.excecoes import RecursoNaoEncontrado


class CadastrarAlternativaService:
    """Caso de uso: cadastrar uma alternativa (cada questão tem só uma correta)."""

    def __init__(self):
        self.repositorio = AlternativaRepository()

    def executar(self, questao_id, texto, correta=False):
        texto = (texto or "").strip()
        if not texto:
            raise ValueError("O texto da alternativa é obrigatório.")

        if Questao.buscar_por_id(questao_id) is None:
            raise RecursoNaoEncontrado("Questão não encontrada.")

        if correta and self.repositorio.contar_corretas_da_questao(questao_id) > 0:
            raise ValueError("Esta questão já tem uma alternativa correta.")

        alternativa = Alternativa(questao_id=questao_id, texto=texto, correta=bool(correta))
        return alternativa.salvar().to_dict()
