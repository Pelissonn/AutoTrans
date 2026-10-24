from models import Simulado
from services.excecoes import RecursoNaoEncontrado


class BuscarSimuladoService:
    """Caso de uso: ver os detalhes de um simulado (somente o dono)."""

    def executar(self, simulado_id, usuario_id_logado):
        simulado = Simulado.buscar_por_id(simulado_id)
        if simulado is None:
            raise RecursoNaoEncontrado("Simulado não encontrado.")

        if not simulado.pertence_a(usuario_id_logado):
            raise PermissionError("Você não tem permissão para ver este simulado.")

        return simulado.to_dict()
