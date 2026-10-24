from repositories import RelatorioRepository


class GerarRelatorioGeralService:
    """Caso de uso: relatório geral da plataforma para o administrador."""

    def __init__(self):
        self.repositorio = RelatorioRepository()

    def executar(self):
        totais = self.repositorio.totais()

        por_categoria = []
        for linha in self.repositorio.resumo_por_categoria():
            simulados = int(linha["simulados"])
            aprovados = int(linha["aprovados"] or 0)
            por_categoria.append({
                "categoria_id": linha["categoria_id"],
                "categoria_nome": linha["categoria_nome"],
                "simulados": simulados,
                "media": round(float(linha["media"]), 1),
                "taxa_aprovacao": round(aprovados / simulados * 100) if simulados else 0,
            })

        return {
            "totais": {
                "usuarios": int(totais["usuarios"]),
                "questoes": int(totais["questoes"]),
                "simulados_finalizados": int(totais["simulados_finalizados"]),
                "media_geral": round(float(totais["media_geral"] or 0), 1),
            },
            "por_categoria": por_categoria,
            "questoes_mais_erradas": self.repositorio.questoes_mais_erradas(),
        }
