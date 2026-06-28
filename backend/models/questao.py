from . import db
from .base import ModeloBase


class Questao(ModeloBase):
    __tablename__ = "questoes"

    categoria_id = db.Column(db.Integer, db.ForeignKey("categorias.id"), nullable=False)
    enunciado = db.Column(db.Text, nullable=False)

    categoria = db.relationship("Categoria", back_populates="questoes")
    alternativas = db.relationship("Alternativa", back_populates="questao")

    def alternativa_correta(self):
        for alternativa in self.alternativas:
            if alternativa.correta:
                return alternativa
        return None
