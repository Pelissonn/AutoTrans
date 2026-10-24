from models import Favorito, Questao
from repositories import FavoritoRepository
from services.excecoes import RecursoNaoEncontrado


class FavoritarQuestaoService:
    """Caso de uso: o aluno marca uma questão para estudar depois."""

    def __init__(self):
        self.repositorio = FavoritoRepository()

    def executar(self, usuario_id, questao_id):
        if not questao_id:
            raise ValueError("Informe a questão que deseja favoritar.")

        if Questao.buscar_por_id(questao_id) is None:
            raise RecursoNaoEncontrado("Questão não encontrada.")

        if self.repositorio.buscar_id(usuario_id, questao_id) is not None:
            raise ValueError("Esta questão já está nos seus favoritos.")

        favorito = Favorito(usuario_id=usuario_id, questao_id=questao_id)
        return favorito.salvar().to_dict()
