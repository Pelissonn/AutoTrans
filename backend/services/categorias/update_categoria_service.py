from models import Categoria


class EditarCategoriaService:
    def executar(self, categoria_id, nome, descricao):
        categoria = Categoria.buscar_por_id(categoria_id)
        if categoria is None:
            raise ValueError("Categoria não encontrada.")

        if not nome or not descricao:
            raise ValueError("Nome e descrição são obrigatórios!")

        categoria.atualizar(nome=nome, descricao=descricao)
        return categoria.to_dict()
