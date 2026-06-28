from . import db
from .base import ModeloBase


class Usuario(ModeloBase):
    __tablename__ = "usuarios"

    nome = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)

    simulados = db.relationship("Simulado", back_populates="usuario")

    @classmethod
    def obter_padrao(cls):
         # Metodo para futura tela de login.
        return cls.query.first()
