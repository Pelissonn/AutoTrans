from . import db
from .base import ModeloBase


class Categoria(ModeloBase):
    __tablename__ = "categorias"

    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(255))

    questoes = db.relationship("Questao", back_populates="categoria")
    materiais = db.relationship("Material", back_populates="categoria")

    # ---------- CRUD (Active Record) ----------
    def salvar(self):
        """CREATE: salva uma nova categoria no banco."""
        db.session.add(self)
        db.session.commit()

    def atualizar(self, nome=None, descricao=None):
        """UPDATE: altera apenas os campos informados."""
        if nome is not None:
            self.nome = nome
        if descricao is not None:
            self.descricao = descricao
        db.session.commit()

    def deletar(self):
        """DELETE: remove a categoria do banco."""
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def listar_todos():
        """READ: retorna todas as categorias."""
        return Categoria.query.order_by(Categoria.nome.asc()).all()

    @staticmethod
    def buscar_por_id(id):
        """READ: busca uma categoria pelo id."""
        return Categoria.query.get(id)

    def to_dict(self):
        """Converte o objeto Categoria para dicionário/JSON."""
        return {
            "id": self.id,
            "nome": self.nome,
            "descricao": self.descricao,
            "total_questoes": len(self.questoes),
        }
