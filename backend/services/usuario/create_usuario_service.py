from models import db, Usuario

class CadastrarUsuarioService:
    def executar(self, nome, email):
        if not nome or not email:
            raise ValueError("Nome e email são obrigatórios.")
        if Usuario.query.filter_by(email=email).first():
            raise ValueError("Email já cadastrado.")
        novo_usuario = Usuario(nome=nome, email=email)
        db.session.add(novo_usuario)
        db.session.commit()