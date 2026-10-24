from . import db


class ModeloBase(db.Model):
    """
    Classe-mãe de todas as entidades do AutoTrans (__abstract__: o
    SQLAlchemy não cria uma tabela para ela).

    Reúne o CRUD feito com o ORM, para que cada Model já nasça sabendo se
    gravar, se alterar e se remover. Os Services usam só estes métodos e
    nunca tocam na sessão do banco. Filtros e relatórios ficam nos
    Repositories, em SQL.
    """

    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)

    @staticmethod
    def _confirmar():
        db.session.commit()

    def salvar(self):
        """Grava um registro novo (INSERT) e devolve o próprio objeto."""
        db.session.add(self)
        self._confirmar()
        return self

    def atualizar(self, **novos_valores):
        """Altera só os campos enviados; valores None são ignorados (UPDATE)."""
        campos_validos = {
            campo: valor
            for campo, valor in novos_valores.items()
            if valor is not None and campo in self.__table__.columns
        }
        for campo, valor in campos_validos.items():
            setattr(self, campo, valor)

        self._confirmar()
        return self

    def deletar(self):
        """Remove o registro (DELETE)."""
        db.session.delete(self)
        self._confirmar()

    @classmethod
    def listar_todos(cls):
        """Todos os registros da tabela, do mais antigo para o mais novo."""
        return db.session.scalars(db.select(cls).order_by(cls.id)).all()

    @classmethod
    def buscar_por_id(cls, id):
        """O registro com esse id, ou None."""
        return db.session.get(cls, id)
