from datetime import datetime

from . import db
from .base import ModeloBase


class Resultado(ModeloBase):
    __tablename__ = "resultados"

    simulado_id = db.Column(db.Integer, db.ForeignKey("simulados.id"), nullable=False)
    nota = db.Column(db.Float, nullable=False, default=0.0)
    data_resultado = db.Column(db.DateTime, default=datetime.now, nullable=False)

    @classmethod
    def buscar_por_simulado(cls, simulado_id):
        return cls.query.filter_by(simulado_id=simulado_id).first()
