from models import db, Usuario

class EditarUsuarioService:
    def executar(self, usuario_id, nome, email):
        usuario = Usuario.query.get(usuario_id)
        if not usuario:
            raise ValueError("Usuario não encontrado.")
            
        if not nome or not email:
            raise ValueError("Nome e e-mail são obrigatórios!")
        
        usuario_existente = Usuario.query.filter_by(email=email).first()
        if usuario_existente and usuario_existente.id != usuario_id:
            raise ValueError("Este e-mail já está em uso por outro usuario.")

        usuario.nome = nome
        usuario.email = email
        db.session.commit()