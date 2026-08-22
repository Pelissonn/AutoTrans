from models import Usuario


class ListarUsuariosService:
    def executar(self):
        usuarios = Usuario.listar_todos()
        return [usuario.to_dict() for usuario in usuarios]


class BuscarUsuarioPorIdService:
    def executar(self, usuario_id):
        usuario = Usuario.buscar_por_id(usuario_id)
        if usuario is None:
            return None
        return usuario.to_dict()
