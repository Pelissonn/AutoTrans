from models import Categoria, Simulado


class DeletarCategoriaService:
    def executar(self, categoria_id):
        categoria = Categoria.buscar_por_id(categoria_id)
        if categoria is None:
            raise ValueError("Categoria não encontrada.")

        total_simulados = Simulado.query.filter_by(categoria_id=categoria_id).count()
        if total_simulados > 0:
            raise ValueError(
                "Não é possível excluir esta categoria: existem "
                f"{total_simulados} simulado(s) de alunos vinculados a ela. "
                "Excluir a categoria apagaria o histórico desses alunos."
            )

        categoria.deletar()
        return True
