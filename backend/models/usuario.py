from datetime import datetime
from . import db
from .base import ModeloBase


class Usuario(ModeloBase):
    __tablename__ = "usuarios"

    nome = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)

    data_criacao = db.Column(db.DateTime, default=datetime.now, nullable=False)
    data_atualizacao = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)

    simulados = db.relationship("Simulado", back_populates="usuario")

    @classmethod
    def obter_padrao(cls):
         # Metodo para futura tela de login.
        return cls.query.first()
