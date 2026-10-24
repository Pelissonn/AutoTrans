from .base_repository import BaseRepository


class ProgressoRepository(BaseRepository):
    """Progresso do aluno por categoria e dias de estudo (sequência)."""

    def progresso_por_categoria(self, usuario_id):
        """
        Para cada categoria: total de questões e quantas questões DIFERENTES
        o aluno já acertou nela (só simulados finalizados).
        """
        return self._buscar_todos(
            """
            SELECT c.id AS categoria_id, c.nome AS categoria_nome,
                   (SELECT COUNT(*) FROM questoes q WHERE q.categoria_id = c.id) AS total_questoes,
                   (SELECT COUNT(DISTINCT i.questao_id)
                      FROM itens_simulado i
                      JOIN simulados s ON s.id = i.simulado_id
                      JOIN resultados r ON r.simulado_id = s.id
                      JOIN questoes q2 ON q2.id = i.questao_id
                     WHERE s.usuario_id = :usuario_id
                       AND q2.categoria_id = c.id
                       AND i.acerto = :verdadeiro) AS questoes_acertadas
            FROM categorias c
            ORDER BY c.nome
            """,
            {"usuario_id": usuario_id, "verdadeiro": True},
        )

    def listar_dias_de_estudo(self, usuario_id):
        """Dias (sem repetir) em que o aluno finalizou simulados, do mais novo ao mais antigo."""
        linhas = self._buscar_todos(
            """
            SELECT DISTINCT DATE(r.data_resultado) AS dia
            FROM resultados r
            JOIN simulados s ON s.id = r.simulado_id
            WHERE s.usuario_id = :usuario_id
            ORDER BY dia DESC
            """,
            {"usuario_id": usuario_id},
        )
        return [linha["dia"] for linha in linhas]
