from models import Usuario

class ListarUsuariosService:
    def executar(self):
        return Usuario.query.all()