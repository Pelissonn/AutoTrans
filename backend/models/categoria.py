from . import db
from .base import ModeloBase


class Categoria(ModeloBase):
    __tablename__ = "categorias"

    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(255))

    questoes = db.relationship("Questao", back_populates="categoria")
    materiais = db.relationship("Material", back_populates="categoria")

    @classmethod
    def listar(cls):
        return cls.query.order_by(cls.nome).all()
