from models import Categoria


class CadastrarCategoriaService:
    def executar(self, nome, descricao=None):
        if not nome:
            raise ValueError("O nome da categoria é obrigatório.")

        categoria = Categoria(nome=nome, descricao=descricao)
        categoria.salvar()
        return categoria.to_dict()
