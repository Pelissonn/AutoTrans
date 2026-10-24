from models import Usuario


class ListarUsuariosService:
    """Caso de uso: listar todos os usuários (administrador)."""

    def executar(self):
        return [usuario.to_dict() for usuario in Usuario.listar_todos()]
