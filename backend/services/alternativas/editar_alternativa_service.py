from models import Alternativa
from repositories import AlternativaRepository
from services.excecoes import RecursoNaoEncontrado


class EditarAlternativaService:
    """Caso de uso: editar o texto ou marcar/desmarcar a alternativa como correta."""

    def __init__(self):
        self.repositorio = AlternativaRepository()

    def executar(self, alternativa_id, texto, correta=None):
        alternativa = Alternativa.buscar_por_id(alternativa_id)
        if alternativa is None:
            raise RecursoNaoEncontrado("Alternativa não encontrada.")

        texto = (texto or "").strip()
        if not texto:
            raise ValueError("O texto da alternativa é obrigatório.")

        if correta and self.repositorio.contar_corretas_da_questao(
            alternativa.questao_id, ignorar_id=alternativa.id
        ) > 0:
            raise ValueError("Esta questão já tem outra alternativa correta.")

        alternativa.atualizar(texto=texto, correta=bool(correta) if correta is not None else None)
        return alternativa.to_dict()
