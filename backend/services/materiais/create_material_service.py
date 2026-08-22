from models import Categoria, Material


class CadastrarMaterialService:
    def executar(self, categoria_id, conteudo, url=None):
        if not conteudo:
            raise ValueError("O conteúdo do material é obrigatório.")

        categoria = Categoria.buscar_por_id(categoria_id)
        if categoria is None:
            raise ValueError("Categoria não encontrada.")

        material = Material(categoria_id=categoria_id, conteudo=conteudo, url=url)
        material.salvar()
        return material.to_dict()
