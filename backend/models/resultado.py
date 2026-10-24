from datetime import datetime

from . import db
from .base import ModeloBase


class Resultado(ModeloBase):
    __tablename__ = "resultados"

    simulado_id = db.Column(
        db.Integer, db.ForeignKey("simulados.id"), unique=True, nullable=False
    )
    nota = db.Column(db.Float, nullable=False, default=0.0)
    data_resultado = db.Column(db.DateTime, default=datetime.now, nullable=False)

    simulado = db.relationship("Simulado", back_populates="resultado")

    def aprovado(self, pontuacao_max):
        """Aprovado = nota igual ou maior que 70% da pontuação máxima."""
        return self.nota >= pontuacao_max * 0.7

    def to_dict(self):
        return {
            "id": self.id,
            "simulado_id": self.simulado_id,
            "nota": self.nota,
            "data_resultado": self.data_resultado.isoformat(),
        }

    def __repr__(self):
        return f"<Resultado {self.id}>"
