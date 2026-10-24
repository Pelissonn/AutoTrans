from models import Categoria
from repositories import CategoriaRepository


class CadastrarCategoriaService:
    """Caso de uso: cadastrar uma categoria (trilha) de estudo."""

    def __init__(self):
        self.repositorio = CategoriaRepository()

    def executar(self, nome, descricao=None):
        nome = (nome or "").strip()
        if not nome:
            raise ValueError("O nome da categoria é obrigatório.")

        if self.repositorio.buscar_id_por_nome(nome) is not None:
            raise ValueError("Já existe uma categoria com este nome.")

        categoria = Categoria(nome=nome, descricao=(descricao or "").strip() or None)
        return categoria.salvar().to_dict()
