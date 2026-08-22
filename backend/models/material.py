from . import db
from .base import ModeloBase


class Material(ModeloBase):
    __tablename__ = "materiais"

    categoria_id = db.Column(db.Integer, db.ForeignKey("categorias.id"), nullable=False)
    conteudo = db.Column(db.Text, nullable=False)
    url = db.Column(db.String(255))

    categoria = db.relationship("Categoria", back_populates="materiais")

    # ---------- CRUD (Active Record) ----------
    def salvar(self):
        """CREATE: salva um novo material no banco."""
        db.session.add(self)
        db.session.commit()

    def atualizar(self, conteudo=None, url=None, categoria_id=None):
        """UPDATE: altera apenas os campos informados."""
        if conteudo is not None:
            self.conteudo = conteudo
        if url is not None:
            self.url = url
        if categoria_id is not None:
            self.categoria_id = categoria_id
        db.session.commit()

    def deletar(self):
        """DELETE: remove o material do banco."""
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def listar_todos():
        """READ: retorna todos os materiais."""
        return Material.query.order_by(Material.id.asc()).all()

    @staticmethod
    def buscar_por_id(id):
        """READ: busca um material pelo id."""
        return Material.query.get(id)

    @staticmethod
    def listar_por_categoria(categoria_id):
        """READ auxiliar: materiais de uma categoria específica."""
        return Material.query.filter_by(categoria_id=categoria_id).all()

    def to_dict(self):
        """Converte o objeto Material para dicionário/JSON."""
        return {
            "id": self.id,
            "categoria_id": self.categoria_id,
            "categoria_nome": self.categoria.nome if self.categoria else None,
            "conteudo": self.conteudo,
            "url": self.url,
        }
