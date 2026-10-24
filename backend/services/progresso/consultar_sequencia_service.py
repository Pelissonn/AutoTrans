from datetime import date

from repositories import ProgressoRepository


class ConsultarSequenciaService:
    """Caso de uso: sequência de dias seguidos de estudo (🔥 streak)."""

    def __init__(self):
        self.repositorio = ProgressoRepository()

    def executar(self, usuario_id, hoje=None):
        hoje = hoje or date.today()
        dias = [self._para_data(d) for d in self.repositorio.listar_dias_de_estudo(usuario_id)]

        return {
            "sequencia_atual": self._sequencia_atual(dias, hoje),
            "maior_sequencia": self._maior_sequencia(dias),
            "total_dias_estudados": len(dias),
        }

    def _para_data(self, valor):
        # SQLite devolve 'AAAA-MM-DD' (texto); MySQL devolve um objeto date.
        return valor if isinstance(valor, date) else date.fromisoformat(str(valor)[:10])

    def _sequencia_atual(self, dias, hoje):
        """Dias seguidos até hoje. Se o último estudo foi ontem, a sequência ainda vale."""
        if not dias or (hoje - dias[0]).days > 1:
            return 0

        sequencia = 1
        for anterior, atual in zip(dias, dias[1:]):
            if (anterior - atual).days != 1:
                break
            sequencia += 1
        return sequencia

    def _maior_sequencia(self, dias):
        maior = atual = 0
        anterior = None
        for dia in reversed(dias):  # do mais antigo para o mais novo
            atual = atual + 1 if anterior and (dia - anterior).days == 1 else 1
            maior = max(maior, atual)
            anterior = dia
        return maior
