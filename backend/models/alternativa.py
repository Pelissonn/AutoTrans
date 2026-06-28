from . import db
from .base import ModeloBase


class Alternativa(ModeloBase):
    __tablename__ = "alternativas"

    questao_id = db.Column(db.Integer, db.ForeignKey("questoes.id"), nullable=False)
    texto = db.Column(db.String(255), nullable=False)
    correta = db.Column(db.Boolean, nullable=False, default=False)

    questao = db.relationship("Questao", back_populates="alternativas")
