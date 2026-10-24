from models import Favorito
from repositories import FavoritoRepository
from services.excecoes import RecursoNaoEncontrado


class RemoverFavoritoService:
    """Caso de uso: o aluno tira uma questão dos favoritos (só os dele)."""

    def __init__(self):
        self.repositorio = FavoritoRepository()

    def executar(self, usuario_id, questao_id):
        favorito_id = self.repositorio.buscar_id(usuario_id, questao_id)
        if favorito_id is None:
            raise RecursoNaoEncontrado("Esta questão não está nos seus favoritos.")

        Favorito.buscar_por_id(favorito_id).deletar()
        return {"mensagem": "Questão removida dos favoritos."}
