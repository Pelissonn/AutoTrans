from . import db
from .base import ModeloBase


class Questao(ModeloBase):
    __tablename__ = "questoes"

    categoria_id = db.Column(db.Integer, db.ForeignKey("categorias.id"), nullable=False)
    enunciado = db.Column(db.Text, nullable=False)

    categoria = db.relationship("Categoria", back_populates="questoes")
    alternativas = db.relationship(
        "Alternativa", back_populates="questao", cascade="all, delete-orphan"
    )

    # ---------- CRUD (Active Record) ----------
    def salvar(self):
        """CREATE: salva uma nova questão no banco."""
        db.session.add(self)
        db.session.commit()

    def atualizar(self, enunciado=None, categoria_id=None):
        """UPDATE: altera apenas os campos informados."""
        if enunciado is not None:
            self.enunciado = enunciado
        if categoria_id is not None:
            self.categoria_id = categoria_id
        db.session.commit()

    def deletar(self):
        """DELETE: remove a questão do banco (junto com as alternativas)."""
        for alternativa in list(self.alternativas):
            db.session.delete(alternativa)
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def listar_todos():
        """READ: retorna todas as questões."""
        return Questao.query.order_by(Questao.id.asc()).all()

    @staticmethod
    def buscar_por_id(id):
        """READ: busca uma questão pelo id."""
        return Questao.query.get(id)

    @staticmethod
    def listar_por_categoria(categoria_id):
        """READ auxiliar: questões de uma categoria específica."""
        return Questao.query.filter_by(categoria_id=categoria_id).all()

    # ---------- CRUD (Active Record) ----------
    def salvar(self):
        """CREATE: salva uma nova questão no banco."""
        db.session.add(self)
        db.session.commit()

    def atualizar(self, enunciado=None, categoria_id=None):
        """UPDATE: altera apenas os campos informados."""
        if enunciado is not None:
            self.enunciado = enunciado
        if categoria_id is not None:
            self.categoria_id = categoria_id
        db.session.commit()

    def deletar(self):
        """DELETE: remove a questão do banco (junto com as alternativas)."""
        for alternativa in list(self.alternativas):
            db.session.delete(alternativa)
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def listar_todos():
        """READ: retorna todas as questões."""
        return Questao.query.order_by(Questao.id.asc()).all()

    @staticmethod
    def buscar_por_id(id):
        """READ: busca uma questão pelo id."""
        return Questao.query.get(id)

    @staticmethod
    def listar_por_categoria(categoria_id):
        """READ auxiliar: questões de uma categoria específica."""
        return Questao.query.filter_by(categoria_id=categoria_id).all()

    def alternativa_correta(self):
        for alternativa in self.alternativas:
            if alternativa.correta:
                return alternativa
        return None

    def to_dict(self, incluir_alternativas=True):
        """Converte o objeto Questao para dicionário/JSON."""
        dados = {
            "id": self.id,
            "categoria_id": self.categoria_id,
            "categoria_nome": self.categoria.nome if self.categoria else None,
            "enunciado": self.enunciado,
        }
        if incluir_alternativas:
            dados["alternativas"] = [a.to_dict() for a in self.alternativas]
        return dados
