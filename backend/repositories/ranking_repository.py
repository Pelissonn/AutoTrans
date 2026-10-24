from .base_repository import BaseRepository


class RankingRepository(BaseRepository):
    """Ranking dos alunos pela média das notas dos simulados finalizados."""

    def listar_ranking(self):
        """
        Uma linha por aluno que já finalizou ao menos um simulado, da melhor
        média para a pior. Em caso de empate, vence quem fez mais simulados.
        """
        return self._buscar_todos(
            """
            SELECT u.id AS usuario_id, u.nome, u.foto_url,
                   AVG(r.nota) AS media,
                   MAX(r.nota) AS melhor_nota,
                   COUNT(r.id) AS total_simulados
            FROM usuarios u
            JOIN simulados s ON s.usuario_id = u.id
            JOIN resultados r ON r.simulado_id = s.id
            GROUP BY u.id, u.nome, u.foto_url
            ORDER BY media DESC, total_simulados DESC, u.nome
            """
        )
