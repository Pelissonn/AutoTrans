from models import Categoria
from repositories import CategoriaRepository
from services.excecoes import RecursoNaoEncontrado


class ExcluirCategoriaService:
    """
    Caso de uso: excluir uma categoria (questões, alternativas e materiais
    saem em cascata). Bloqueado se algum aluno já fez simulado nela.
    """

    def __init__(self):
        self.repositorio = CategoriaRepository()

    def executar(self, categoria_id):
        categoria = Categoria.buscar_por_id(categoria_id)
        if categoria is None:
            raise RecursoNaoEncontrado("Categoria não encontrada.")

        total_simulados = self.repositorio.contar_simulados(categoria_id)
        if total_simulados > 0:
            raise ValueError(
                f"Não é possível excluir: existem {total_simulados} simulado(s) de alunos "
                "nesta categoria. Excluí-la apagaria o histórico deles."
            )

        categoria.deletar()
        return {"mensagem": "Categoria excluída com sucesso."}
