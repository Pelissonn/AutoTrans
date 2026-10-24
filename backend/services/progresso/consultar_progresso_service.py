from repositories import ProgressoRepository


class ConsultarProgressoService:
    """Caso de uso: percentual de questões dominadas pelo aluno em cada categoria."""

    def __init__(self):
        self.repositorio = ProgressoRepository()

    def executar(self, usuario_id):
        progresso = []
        for linha in self.repositorio.progresso_por_categoria(usuario_id):
            total = linha["total_questoes"] or 0
            acertadas = min(linha["questoes_acertadas"] or 0, total)
            progresso.append({
                "categoria_id": linha["categoria_id"],
                "categoria_nome": linha["categoria_nome"],
                "total_questoes": total,
                "questoes_acertadas": acertadas,
                "percentual": round(acertadas / total * 100) if total else 0,
            })

        return {"categorias": progresso}
