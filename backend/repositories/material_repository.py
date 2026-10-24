from .base_repository import BaseRepository


class MaterialRepository(BaseRepository):
    """Consultas especiais sobre materiais de estudo."""

    def listar_por_categoria(self, categoria_id):
        """Filtro por categoria, já trazendo o nome da categoria (JOIN)."""
        return self._buscar_todos(
            """
            SELECT m.id, m.categoria_id, c.nome AS categoria_nome, m.conteudo, m.url
            FROM materiais m
            JOIN categorias c ON c.id = m.categoria_id
            WHERE m.categoria_id = :categoria_id
            ORDER BY m.id
            """,
            {"categoria_id": categoria_id},
        )
