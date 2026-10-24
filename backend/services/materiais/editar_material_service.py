from models import Categoria, Material
from services.excecoes import RecursoNaoEncontrado


class EditarMaterialService:
    """Caso de uso: editar o conteúdo, o link ou a categoria de um material."""

    def executar(self, material_id, conteudo, url=None, categoria_id=None):
        material = Material.buscar_por_id(material_id)
        if material is None:
            raise RecursoNaoEncontrado("Material não encontrado.")

        conteudo = (conteudo or "").strip()
        if not conteudo:
            raise ValueError("O conteúdo do material é obrigatório.")

        if categoria_id and Categoria.buscar_por_id(categoria_id) is None:
            raise RecursoNaoEncontrado("Categoria não encontrada.")

        material.atualizar(conteudo=conteudo, url=url, categoria_id=categoria_id)
        return material.to_dict()
