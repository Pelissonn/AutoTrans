from datetime import datetime

from . import db
from .base import ModeloBase


class Simulado(ModeloBase):
    __tablename__ = "simulados"

    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey("categorias.id"), nullable=False)
    titulo = db.Column(db.String(150), nullable=False)
    pontuacao_max = db.Column(db.Float, nullable=False, default=100.0)
    data_realizacao = db.Column(db.DateTime, default=datetime.now, nullable=False)

    usuario = db.relationship("Usuario", back_populates="simulados")
    categoria = db.relationship("Categoria")
    itens = db.relationship("ItemSimulado", back_populates="simulado")

    @classmethod
    def buscar_por_id(cls, simulado_id):
        return cls.query.get(simulado_id)

    def calcular_pontuacao(self):
        total = len(self.itens)
        if total == 0:
            return 0.0
        acertos = sum(1 for item in self.itens if item.acerto)
        return round((acertos / total) * self.pontuacao_max, 1)
