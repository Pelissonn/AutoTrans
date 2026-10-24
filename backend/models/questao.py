from . import db
from .base import ModeloBase


class Questao(ModeloBase):
    __tablename__ = "questoes"

    categoria_id = db.Column(db.Integer, db.ForeignKey("categorias.id"), nullable=False)
    enunciado = db.Column(db.Text, nullable=False)

    categoria = db.relationship("Categoria", back_populates="questoes")
    # Composição: as alternativas são apagadas junto com a questão.
    alternativas = db.relationship(
        "Alternativa",
        back_populates="questao",
        cascade="all, delete-orphan",
        order_by="Alternativa.id",
    )
    favoritos = db.relationship(
        "Favorito", back_populates="questao", cascade="all, delete-orphan"
    )

    def alternativa_correta(self):
        for alternativa in self.alternativas:
            if alternativa.correta:
                return alternativa
        return None

    def to_dict(self, incluir_alternativas=True):
        dados = {
            "id": self.id,
            "categoria_id": self.categoria_id,
            "categoria_nome": self.categoria.nome if self.categoria else None,
            "enunciado": self.enunciado,
        }
        if incluir_alternativas:
            dados["alternativas"] = [a.to_dict() for a in self.alternativas]
        return dados

    def __repr__(self):
        return f"<Questao {self.id}>"
