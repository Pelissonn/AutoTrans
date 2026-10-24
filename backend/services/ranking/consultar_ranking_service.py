from repositories import RankingRepository


class ConsultarRankingService:
    """Caso de uso: ranking dos alunos pela média das notas, com a posição do aluno logado."""

    def __init__(self):
        self.repositorio = RankingRepository()

    def executar(self, usuario_id_logado, limite=10):
        ranking = []
        minha_posicao = None

        for posicao, linha in enumerate(self.repositorio.listar_ranking(), start=1):
            if linha["usuario_id"] == usuario_id_logado:
                minha_posicao = posicao

            ranking.append({
                "posicao": posicao,
                "usuario_id": linha["usuario_id"],
                "nome": linha["nome"],
                "foto_url": linha["foto_url"],
                "media": round(float(linha["media"]), 1),
                "melhor_nota": round(float(linha["melhor_nota"]), 1),
                "total_simulados": int(linha["total_simulados"]),
            })

        return {
            "ranking": ranking[:limite],
            "minha_posicao": minha_posicao,
            "total_participantes": len(ranking),
        }
