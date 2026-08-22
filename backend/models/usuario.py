from datetime import datetime

from werkzeug.security import check_password_hash, generate_password_hash

from . import db
from .base import ModeloBase


class Usuario(ModeloBase):
    __tablename__ = "usuarios"

    nome = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    senha_hash = db.Column(db.String(255), nullable=False)
    foto_url = db.Column(db.String(500), nullable=True)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.now, nullable=False)
    data_atualizacao = db.Column(
        db.DateTime, default=datetime.now, onupdate=datetime.now, nullable=False
    )

    simulados = db.relationship("Simulado", back_populates="usuario")

    # ---------- Senha ----------
    def definir_senha(self, senha):
        """Nunca guardamos a senha em texto puro — só o hash dela."""
        self.senha_hash = generate_password_hash(senha)

    def verificar_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)

    # ---------- CRUD (Active Record) ----------
    def salvar(self):
        """CREATE: salva um novo usuário no banco."""
        db.session.add(self)
        db.session.commit()

    def atualizar(self, nome=None, email=None, senha=None, foto_url=None, is_admin=None):
        """UPDATE: altera apenas os campos informados."""
        if nome is not None:
            self.nome = nome
        if email is not None:
            self.email = email
        if senha:
            self.definir_senha(senha)
        if foto_url is not None:
            self.foto_url = foto_url
        if is_admin is not None:
            self.is_admin = is_admin
        db.session.commit()

    def deletar(self):
        """DELETE: remove o usuário do banco."""
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def listar_todos():
        """READ: retorna todos os usuários."""
        return Usuario.query.order_by(Usuario.id.asc()).all()

    @staticmethod
    def buscar_por_id(id):
        """READ: busca um usuário pelo id."""
        return Usuario.query.get(id)

    @staticmethod
    def buscar_por_email(email):
        """READ auxiliar: busca um usuário pelo e-mail."""
        return Usuario.query.filter_by(email=email).first()

    def to_dict(self):
        """Converte o objeto Usuario para dicionário/JSON (nunca inclui a senha)."""
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "foto_url": self.foto_url,
            "is_admin": self.is_admin,
        }
