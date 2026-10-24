from .base_repository import BaseRepository


class SimuladoRepository(BaseRepository):
    """Histórico do aluno: simulados finalizados e estatísticas de desempenho."""

    def listar_historico_por_usuario(self, usuario_id):
        """
        Junta Simulado + Resultado + Categoria, filtra pelo aluno e ordena
        do mais recente para o mais antigo. Só entram simulados finalizados.
        """
        return self._buscar_todos(
            """
            SELECT s.id, s.titulo, s.categoria_id, c.nome AS categoria_nome,
                   s.pontuacao_max, s.data_realizacao,
                   r.id AS resultado_id, r.nota, r.data_resultado,
                   (SELECT COUNT(*) FROM itens_simulado i WHERE i.simulado_id = s.id) AS total_questoes,
                   (SELECT COUNT(*) FROM itens_simulado i
                     WHERE i.simulado_id = s.id AND i.acerto = :verdadeiro) AS total_acertos
            FROM simulados s
            JOIN resultados r ON r.simulado_id = s.id
            JOIN categorias c ON c.id = s.categoria_id
            WHERE s.usuario_id = :usuario_id
            ORDER BY s.data_realizacao DESC, s.id DESC
            """,
            {"usuario_id": usuario_id, "verdadeiro": True},
        )

    def calcular_estatisticas(self, usuario_id):
        """Quantidade, média, melhor e pior nota do aluno (funções de agregação)."""
        return self._buscar_um(
            """
            SELECT COUNT(r.id) AS total_simulados,
                   AVG(r.nota) AS media,
                   MAX(r.nota) AS melhor,
                   MIN(r.nota) AS pior
            FROM resultados r
            JOIN simulados s ON s.id = r.simulado_id
            WHERE s.usuario_id = :usuario_id
            """,
            {"usuario_id": usuario_id},
        )
