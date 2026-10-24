from .base_repository import BaseRepository


class QuestaoRepository(BaseRepository):
    """Consultas especiais sobre questões: filtros, busca e caderno de erros."""

    _SELECT_QUESTAO = """
        SELECT q.id, q.categoria_id, c.nome AS categoria_nome, q.enunciado
        FROM questoes q
        JOIN categorias c ON c.id = q.categoria_id
    """

    def listar_por_categoria(self, categoria_id):
        """Filtro por categoria (com o nome da categoria via JOIN)."""
        return self._buscar_todos(
            self._SELECT_QUESTAO + " WHERE q.categoria_id = :categoria_id ORDER BY q.id",
            {"categoria_id": categoria_id},
        )

    def listar_ids_por_categoria(self, categoria_id):
        """Só os ids das questões da categoria (usado para sortear o simulado)."""
        linhas = self._buscar_todos(
            "SELECT id FROM questoes WHERE categoria_id = :categoria_id ORDER BY id",
            {"categoria_id": categoria_id},
        )
        return [linha["id"] for linha in linhas]

    def buscar_por_palavra(self, palavra, categoria_id=None, limite=50):
        """Busca por palavra-chave no enunciado (LIKE), opcionalmente numa categoria."""
        sql = self._SELECT_QUESTAO + " WHERE LOWER(q.enunciado) LIKE LOWER(:padrao)"
        parametros = {"padrao": f"%{palavra}%", "limite": limite}

        if categoria_id:
            sql += " AND q.categoria_id = :categoria_id"
            parametros["categoria_id"] = categoria_id

        sql += " ORDER BY q.id LIMIT :limite"
        return self._buscar_todos(sql, parametros)

    def buscar_id_por_enunciado(self, categoria_id, enunciado):
        """Localiza uma questão pelo enunciado na categoria (a importação não duplica)."""
        linha = self._buscar_um(
            """
            SELECT id FROM questoes
            WHERE categoria_id = :categoria_id AND enunciado = :enunciado
            """,
            {"categoria_id": categoria_id, "enunciado": enunciado},
        )
        return linha["id"] if linha else None

    def contar_respostas_em_simulados(self, questao_id):
        """Em quantos simulados a questão já apareceu (bloqueia a exclusão)."""
        return self._buscar_valor(
            "SELECT COUNT(*) FROM itens_simulado WHERE questao_id = :questao_id",
            {"questao_id": questao_id},
        )

    def listar_erradas_por_usuario(self, usuario_id, limite=20):
        """
        Caderno de erros: questões que o aluno errou em simulados finalizados,
        da mais errada para a menos errada.
        """
        return self._buscar_todos(
            """
            SELECT q.id, q.categoria_id, c.nome AS categoria_nome, q.enunciado,
                   COUNT(i.id) AS total_erros
            FROM itens_simulado i
            JOIN simulados s ON s.id = i.simulado_id
            JOIN resultados r ON r.simulado_id = s.id
            JOIN questoes q ON q.id = i.questao_id
            JOIN categorias c ON c.id = q.categoria_id
            WHERE s.usuario_id = :usuario_id
              AND i.acerto = :falso
            GROUP BY q.id, q.categoria_id, c.nome, q.enunciado
            ORDER BY total_erros DESC, q.id
            LIMIT :limite
            """,
            {"usuario_id": usuario_id, "falso": False, "limite": limite},
        )
