from . import db
from .base import ModeloBase


class Material(ModeloBase):
    __tablename__ = "materiais"

    categoria_id = db.Column(db.Integer, db.ForeignKey("categorias.id"), nullable=False)
    conteudo = db.Column(db.Text, nullable=False)
    url = db.Column(db.String(255))

    categoria = db.relationship("Categoria", back_populates="materiais")

    def to_dict(self):
        return {
            "id": self.id,
            "categoria_id": self.categoria_id,
            "categoria_nome": self.categoria.nome if self.categoria else None,
            "conteudo": self.conteudo,
            "url": self.url,
        }

    def __repr__(self):
        return f"<Material {self.id}>"
