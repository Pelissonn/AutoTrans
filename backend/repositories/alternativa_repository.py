from .base_repository import BaseRepository


class AlternativaRepository(BaseRepository):
    """Consultas especiais sobre alternativas."""

    def listar_por_questao(self, questao_id):
        """Filtro: alternativas de uma questão específica."""
        linhas = self._buscar_todos(
            """
            SELECT id, questao_id, texto, correta
            FROM alternativas
            WHERE questao_id = :questao_id
            ORDER BY id
            """,
            {"questao_id": questao_id},
        )
        # SQLite devolve 0/1 para booleanos; convertemos para true/false.
        for linha in linhas:
            linha["correta"] = bool(linha["correta"])
        return linhas

    def contar_respostas(self, alternativa_id):
        """Quantas vezes a alternativa já foi escolhida em simulados (bloqueia a exclusão)."""
        return self._buscar_valor(
            "SELECT COUNT(*) FROM itens_simulado WHERE alternativa_escolhida_id = :alternativa_id",
            {"alternativa_id": alternativa_id},
        )

    def contar_corretas_da_questao(self, questao_id, ignorar_id=None):
        """Quantas alternativas corretas a questão já tem (cada questão aceita só uma)."""
        return self._buscar_valor(
            """
            SELECT COUNT(*) FROM alternativas
            WHERE questao_id = :questao_id
              AND correta = :verdadeiro
              AND id <> :ignorar_id
            """,
            {"questao_id": questao_id, "verdadeiro": True, "ignorar_id": ignorar_id or 0},
        )
