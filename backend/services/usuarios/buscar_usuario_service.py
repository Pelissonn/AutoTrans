from models import Usuario
from services.excecoes import RecursoNaoEncontrado


class BuscarUsuarioService:
    """Caso de uso: consultar os dados de um usuário (perfil ou administração)."""

    def executar(self, usuario_id):
        usuario = Usuario.buscar_por_id(usuario_id)
        if usuario is None:
            raise RecursoNaoEncontrado("Usuário não encontrado.")
        return usuario.to_dict()
