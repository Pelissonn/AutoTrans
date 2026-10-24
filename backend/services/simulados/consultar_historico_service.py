from repositories import SimuladoRepository
from utils.datas import para_texto_iso


class ConsultarHistoricoService:
    """Caso de uso: histórico de simulados do aluno com estatísticas de evolução."""

    def __init__(self):
        self.repositorio = SimuladoRepository()

    def executar(self, usuario_id):
        linhas = self.repositorio.listar_historico_por_usuario(usuario_id)
        estatisticas = self.repositorio.calcular_estatisticas(usuario_id)

        simulados = [
            {
                "id": linha["id"],
                "titulo": linha["titulo"],
                "categoria_id": linha["categoria_id"],
                "categoria_nome": linha["categoria_nome"],
                "pontuacao_max": linha["pontuacao_max"],
                "data_realizacao": para_texto_iso(linha["data_realizacao"]),
                "total_questoes": linha["total_questoes"],
                "total_acertos": linha["total_acertos"],
                "resultado": {
                    "id": linha["resultado_id"],
                    "nota": linha["nota"],
                    "data_resultado": para_texto_iso(linha["data_resultado"]),
                },
            }
            for linha in linhas
        ]

        return {"estatisticas": self._formatar(estatisticas), "simulados": simulados}

    def _formatar(self, estatisticas):
        if not estatisticas or not estatisticas["total_simulados"]:
            return {"media": 0, "melhor": 0, "pior": 0, "total_simulados": 0}

        return {
            "media": round(float(estatisticas["media"]), 1),
            "melhor": round(float(estatisticas["melhor"]), 1),
            "pior": round(float(estatisticas["pior"]), 1),
            "total_simulados": int(estatisticas["total_simulados"]),
        }
