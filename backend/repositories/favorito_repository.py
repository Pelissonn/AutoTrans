from .base_repository import BaseRepository


class FavoritoRepository(BaseRepository):
    """Consultas especiais sobre as questões favoritas de cada aluno."""

    def listar_questoes_favoritas(self, usuario_id):
        """Questões favoritadas pelo aluno (as mais recentes primeiro)."""
        return self._buscar_todos(
            """
            SELECT f.id AS favorito_id, f.data_criacao,
                   q.id, q.categoria_id, c.nome AS categoria_nome, q.enunciado
            FROM favoritos f
            JOIN questoes q ON q.id = f.questao_id
            JOIN categorias c ON c.id = q.categoria_id
            WHERE f.usuario_id = :usuario_id
            ORDER BY f.id DESC
            """,
            {"usuario_id": usuario_id},
        )

    def buscar_id(self, usuario_id, questao_id):
        """Localiza o favorito de um aluno para uma questão (ou None)."""
        linha = self._buscar_um(
            """
            SELECT id FROM favoritos
            WHERE usuario_id = :usuario_id AND questao_id = :questao_id
            """,
            {"usuario_id": usuario_id, "questao_id": questao_id},
        )
        return linha["id"] if linha else None
