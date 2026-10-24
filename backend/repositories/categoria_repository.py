from .base_repository import BaseRepository


class CategoriaRepository(BaseRepository):
    """Consultas especiais sobre categorias."""

    def buscar_id_por_nome(self, nome):
        """Localiza uma categoria pelo nome (usado na importação, para não duplicar)."""
        linha = self._buscar_um(
            "SELECT id FROM categorias WHERE LOWER(nome) = LOWER(:nome)",
            {"nome": nome},
        )
        return linha["id"] if linha else None

    def contar_simulados(self, categoria_id):
        """Quantos simulados de alunos usam esta categoria (bloqueia a exclusão)."""
        return self._buscar_valor(
            "SELECT COUNT(*) FROM simulados WHERE categoria_id = :categoria_id",
            {"categoria_id": categoria_id},
        )
