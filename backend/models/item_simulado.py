from . import db
from .base import ModeloBase


class ItemSimulado(ModeloBase):
    """Cada questão de um Simulado, junto com a resposta marcada pelo aluno."""

    __tablename__ = "itens_simulado"

    simulado_id = db.Column(db.Integer, db.ForeignKey("simulados.id"), nullable=False)
    questao_id = db.Column(db.Integer, db.ForeignKey("questoes.id"), nullable=False)
    alternativa_escolhida_id = db.Column(db.Integer, db.ForeignKey("alternativas.id"))
    acerto = db.Column(db.Boolean, nullable=False, default=False)

    simulado = db.relationship("Simulado", back_populates="itens")
    questao = db.relationship("Questao")
    alternativa_escolhida = db.relationship("Alternativa")

    def corrigir(self):
        """Compara a alternativa escolhida com a correta da questão (não grava)."""
        correta = self.questao.alternativa_correta() if self.questao else None
        self.acerto = bool(correta and self.alternativa_escolhida_id == correta.id)
        return self.acerto

    def to_dict(self):
        return {
            "id": self.id,
            "simulado_id": self.simulado_id,
            "questao": self.questao.to_dict() if self.questao else None,
            "alternativa_escolhida_id": self.alternativa_escolhida_id,
            "alternativa_escolhida_texto": (
                self.alternativa_escolhida.texto if self.alternativa_escolhida else None
            ),
            "acerto": self.acerto,
        }

    def __repr__(self):
        return f"<ItemSimulado {self.id}>"
