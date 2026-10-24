from flask import jsonify, request
from flask.views import MethodView

from services.excecoes import RecursoNaoEncontrado, ServicoExternoIndisponivel

# Erros de regra de negócio que os Services podem lançar.
ERROS_DE_NEGOCIO = (ValueError, PermissionError, ServicoExternoIndisponivel)


class BaseController(MethodView):
    """
    Classe-mãe dos Controllers (cada Controller é uma classe ligada a um
    recurso do sistema). O Controller só:
      1. recebe a requisição HTTP e lê os dados (JSON, query string, URL);
      2. chama o Service do caso de uso;
      3. devolve a resposta JSON com o status HTTP certo.
    Regra de negócio fica no Service; acesso a dados, na Model/Repository.
    """

    @classmethod
    def registrar_crud(cls, blueprint, nome):
        """
        Liga a classe às rotas padrão de um recurso:
          /       -> GET (listar) e POST (cadastrar)
          /<id>   -> GET (consultar), PUT (editar) e DELETE (excluir)
        O método get(self, id=None) sabe se veio ou não um id.
        """
        view = cls.as_view(nome)
        blueprint.add_url_rule("/", view_func=view, methods=["GET", "POST"])
        blueprint.add_url_rule("/<int:id>", view_func=view, methods=["GET", "PUT", "DELETE"])
        return view

    @staticmethod
    def dados_json():
        return request.get_json(silent=True) or {}

    @staticmethod
    def responder(dados, status=200):
        return jsonify(dados), status

    @staticmethod
    def responder_erro(erro):
        if isinstance(erro, RecursoNaoEncontrado):
            status = 404
        elif isinstance(erro, PermissionError):
            status = 403
        elif isinstance(erro, ServicoExternoIndisponivel):
            status = 503
        else:
            status = 400
        return jsonify({"erro": str(erro)}), status
