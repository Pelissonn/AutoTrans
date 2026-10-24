from models import Categoria, Material
from services.excecoes import RecursoNaoEncontrado


class CadastrarMaterialService:
    """Caso de uso: cadastrar um material de estudo em uma categoria."""

    def executar(self, categoria_id, conteudo, url=None):
        conteudo = (conteudo or "").strip()
        if not conteudo:
            raise ValueError("O conteúdo do material é obrigatório.")

        if Categoria.buscar_por_id(categoria_id) is None:
            raise RecursoNaoEncontrado("Categoria não encontrada.")

        material = Material(
            categoria_id=categoria_id,
            conteudo=conteudo,
            url=(url or "").strip() or None,
        )
        return material.salvar().to_dict()
