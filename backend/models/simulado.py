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
    # Agregação: o simulado usa a categoria, mas não é dono dela.
    categoria = db.relationship("Categoria")
    # Composição: itens e resultado só existem dentro do simulado.
    itens = db.relationship(
        "ItemSimulado",
        back_populates="simulado",
        cascade="all, delete-orphan",
        order_by="ItemSimulado.id",
    )
    resultado = db.relationship(
        "Resultado", back_populates="simulado", uselist=False, cascade="all, delete-orphan"
    )

    def calcular_pontuacao(self):
        total = len(self.itens)
        if total == 0:
            return 0.0
        acertos = sum(1 for item in self.itens if item.acerto)
        return round((acertos / total) * self.pontuacao_max, 1)

    def pertence_a(self, usuario_id):
        return self.usuario_id == usuario_id

    def to_dict(self, incluir_itens=True):
        dados = {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "categoria_id": self.categoria_id,
            "titulo": self.titulo,
            "pontuacao_max": self.pontuacao_max,
            "data_realizacao": self.data_realizacao.isoformat(),
            "resultado": self.resultado.to_dict() if self.resultado else None,
        }
        if incluir_itens:
            dados["itens"] = [item.to_dict() for item in self.itens]
        return dados

    def __repr__(self):
        return f"<Simulado {self.id}>"
