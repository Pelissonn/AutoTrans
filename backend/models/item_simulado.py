from . import db
from .base import ModeloBase


class ItemSimulado(ModeloBase):
    __tablename__ = "itens_simulado"

    simulado_id = db.Column(db.Integer, db.ForeignKey("simulados.id"), nullable=False)
    questao_id = db.Column(db.Integer, db.ForeignKey("questoes.id"), nullable=False)
    alternativa_escolhida_id = db.Column(db.Integer, db.ForeignKey("alternativas.id"))
    acerto = db.Column(db.Boolean, nullable=False, default=False)

    simulado = db.relationship("Simulado", back_populates="itens")
    questao = db.relationship("Questao")
    alternativa_escolhida = db.relationship("Alternativa")

    def verificar(self):
        correta = self.questao.alternativa_correta()
        self.acerto = bool(correta and self.alternativa_escolhida_id == correta.id)
        return self.acerto
