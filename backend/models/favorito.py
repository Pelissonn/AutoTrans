from datetime import datetime

from . import db
from .base import ModeloBase


class Favorito(ModeloBase):
    """Questão que o aluno marcou com uma estrela para estudar depois."""

    __tablename__ = "favoritos"
    __table_args__ = (
        # O mesmo aluno não pode favoritar a mesma questão duas vezes.
        db.UniqueConstraint("usuario_id", "questao_id", name="uq_favorito_usuario_questao"),
    )

    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    questao_id = db.Column(db.Integer, db.ForeignKey("questoes.id"), nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.now, nullable=False)

    usuario = db.relationship("Usuario", back_populates="favoritos")
    questao = db.relationship("Questao", back_populates="favoritos")

    def to_dict(self):
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "questao_id": self.questao_id,
            "data_criacao": self.data_criacao.isoformat(),
            "questao": self.questao.to_dict() if self.questao else None,
        }

    def __repr__(self):
        return f"<Favorito {self.id}>"
