from . import db
from .base import ModeloBase


class Categoria(ModeloBase):
    __tablename__ = "categorias"

    nome = db.Column(db.String(100), unique=True, nullable=False)
    descricao = db.Column(db.String(255))

    # Composição: questões e materiais não existem sem a categoria.
    questoes = db.relationship(
        "Questao", back_populates="categoria", cascade="all, delete-orphan"
    )
    materiais = db.relationship(
        "Material", back_populates="categoria", cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "descricao": self.descricao,
            "total_questoes": len(self.questoes),
        }

    def __repr__(self):
        return f"<Categoria {self.nome}>"
