from . import db
from .base import ModeloBase


class Alternativa(ModeloBase):
    __tablename__ = "alternativas"

    questao_id = db.Column(db.Integer, db.ForeignKey("questoes.id"), nullable=False)
    texto = db.Column(db.String(255), nullable=False)
    correta = db.Column(db.Boolean, nullable=False, default=False)

    questao = db.relationship("Questao", back_populates="alternativas")

    # ---------- CRUD (Active Record) ----------
    def salvar(self):
        """CREATE: salva uma nova alternativa no banco."""
        db.session.add(self)
        db.session.commit()

    def atualizar(self, texto=None, correta=None, questao_id=None):
        """UPDATE: altera apenas os campos informados."""
        if texto is not None:
            self.texto = texto
        if correta is not None:
            self.correta = correta
        if questao_id is not None:
            self.questao_id = questao_id
        db.session.commit()

    def deletar(self):
        """DELETE: remove a alternativa do banco."""
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def listar_todos():
        """READ: retorna todas as alternativas."""
        return Alternativa.query.order_by(Alternativa.id.asc()).all()

    @staticmethod
    def buscar_por_id(id):
        """READ: busca uma alternativa pelo id."""
        return Alternativa.query.get(id)

    @staticmethod
    def listar_por_questao(questao_id):
        """READ auxiliar: alternativas de uma questão específica."""
        return Alternativa.query.filter_by(questao_id=questao_id).all()

    def to_dict(self):
        """Converte o objeto Alternativa para dicionário/JSON."""
        return {
            "id": self.id,
            "questao_id": self.questao_id,
            "texto": self.texto,
            "correta": self.correta,
        }
