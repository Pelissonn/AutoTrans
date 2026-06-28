from . import db
from .base import ModeloBase


class Material(ModeloBase):
    __tablename__ = "materiais"

    categoria_id = db.Column(db.Integer, db.ForeignKey("categorias.id"), nullable=False)
    conteudo = db.Column(db.Text, nullable=False)
    url = db.Column(db.String(255))

    categoria = db.relationship("Categoria", back_populates="materiais")
