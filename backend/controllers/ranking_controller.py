from flask import Blueprint, request

from controllers.base_controller import BaseController
from services.ranking import ConsultarRankingService
from utils.auth import login_obrigatorio

ranking_bp = Blueprint("ranking", __name__, url_prefix="/ranking")


class RankingController(BaseController):
    """GET /ranking/ — ranking dos alunos e a posição do aluno logado."""

    decorators = [login_obrigatorio]

    def get(self):
        return self.responder(ConsultarRankingService().executar(request.usuario_id))


ranking_bp.add_url_rule("/", view_func=RankingController.as_view("ranking_api"), methods=["GET"])
