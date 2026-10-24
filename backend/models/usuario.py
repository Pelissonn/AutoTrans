from datetime import datetime

from werkzeug.security import check_password_hash, generate_password_hash

from . import db
from .base import ModeloBase


class Usuario(ModeloBase):
    __tablename__ = "usuarios"

    nome = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(255), nullable=False)
    foto_url = db.Column(db.String(500), nullable=True)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    # Termo de consentimento: decisão do usuário registrada no cadastro.
    aceitou_termos = db.Column(db.Boolean, default=False, nullable=False)
    data_aceite_termos = db.Column(db.DateTime, nullable=True)
    data_criacao = db.Column(db.DateTime, default=datetime.now, nullable=False)
    data_atualizacao = db.Column(
        db.DateTime, default=datetime.now, onupdate=datetime.now, nullable=False
    )

    # Excluir o usuário apaga também o histórico dele (simulados, itens,
    # resultados e favoritos) — são dados do próprio aluno.
    simulados = db.relationship(
        "Simulado", back_populates="usuario", cascade="all, delete-orphan"
    )
    favoritos = db.relationship(
        "Favorito", back_populates="usuario", cascade="all, delete-orphan"
    )

    def definir_senha(self, senha):
        """Nunca guardamos a senha em texto puro — só o hash dela."""
        self.senha_hash = generate_password_hash(senha)

    def verificar_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)

    def registrar_aceite_termos(self):
        self.aceitou_termos = True
        self.data_aceite_termos = datetime.now()

    def to_dict(self):
        """Converte para dicionário/JSON (nunca inclui a senha)."""
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "foto_url": self.foto_url,
            "is_admin": self.is_admin,
            "aceitou_termos": self.aceitou_termos,
            "data_aceite_termos": (
                self.data_aceite_termos.isoformat() if self.data_aceite_termos else None
            ),
            "data_criacao": self.data_criacao.isoformat() if self.data_criacao else None,
        }

    def __repr__(self):
        return f"<Usuario {self.email}>"
