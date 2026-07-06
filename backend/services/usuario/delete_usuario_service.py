from models import db, Usuario

class DeletarUsuarioService:
    def executar(self, usuario_id):
        usuario = Usuario.query.get(usuario_id)
        if not usuario:
            raise ValueError("Usuario não encontrado.")
        db.session.delete(usuario)
        db.session.commit()