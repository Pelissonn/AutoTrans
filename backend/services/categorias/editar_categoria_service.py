from models import Categoria
from repositories import CategoriaRepository
from services.excecoes import RecursoNaoEncontrado


class EditarCategoriaService:
    """Caso de uso: editar nome e descrição de uma categoria."""

    def __init__(self):
        self.repositorio = CategoriaRepository()

    def executar(self, categoria_id, nome, descricao=None):
        categoria = Categoria.buscar_por_id(categoria_id)
        if categoria is None:
            raise RecursoNaoEncontrado("Categoria não encontrada.")

        nome = (nome or "").strip()
        if not nome:
            raise ValueError("O nome da categoria é obrigatório.")

        outro_id = self.repositorio.buscar_id_por_nome(nome)
        if outro_id is not None and outro_id != categoria.id:
            raise ValueError("Já existe outra categoria com este nome.")

        categoria.atualizar(nome=nome, descricao=descricao)
        return categoria.to_dict()
