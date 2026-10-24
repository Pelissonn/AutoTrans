from .base_repository import BaseRepository


class RelatorioRepository(BaseRepository):
    """Relatório geral da plataforma (administrador): totais e agrupamentos."""

    def totais(self):
        return self._buscar_um(
            """
            SELECT (SELECT COUNT(*) FROM usuarios) AS usuarios,
                   (SELECT COUNT(*) FROM questoes) AS questoes,
                   (SELECT COUNT(*) FROM resultados) AS simulados_finalizados,
                   (SELECT AVG(nota) FROM resultados) AS media_geral
            """
        )

    def resumo_por_categoria(self):
        """Simulados finalizados, média e taxa de aprovação por categoria."""
        return self._buscar_todos(
            """
            SELECT c.id AS categoria_id, c.nome AS categoria_nome,
                   COUNT(r.id) AS simulados,
                   AVG(r.nota) AS media,
                   SUM(CASE WHEN r.nota >= s.pontuacao_max * 0.7 THEN 1 ELSE 0 END) AS aprovados
            FROM categorias c
            JOIN simulados s ON s.categoria_id = c.id
            JOIN resultados r ON r.simulado_id = s.id
            GROUP BY c.id, c.nome
            ORDER BY c.nome
            """
        )

    def questoes_mais_erradas(self, limite=5):
        """As questões com mais erros em toda a plataforma."""
        return self._buscar_todos(
            """
            SELECT q.id AS questao_id, q.enunciado, c.nome AS categoria_nome,
                   COUNT(i.id) AS erros
            FROM itens_simulado i
            JOIN simulados s ON s.id = i.simulado_id
            JOIN resultados r ON r.simulado_id = s.id
            JOIN questoes q ON q.id = i.questao_id
            JOIN categorias c ON c.id = q.categoria_id
            WHERE i.acerto = :falso
            GROUP BY q.id, q.enunciado, c.nome
            ORDER BY erros DESC, q.id
            LIMIT :limite
            """,
            {"falso": False, "limite": limite},
        )
