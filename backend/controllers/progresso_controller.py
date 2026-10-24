from flask import Blueprint, request

from controllers.base_controller import BaseController
from services.progresso import ConsultarProgressoService, ConsultarSequenciaService
from utils.auth import login_obrigatorio

progresso_bp = Blueprint("progresso", __name__, url_prefix="/progresso")


class ProgressoController(BaseController):
    """GET /progresso/ — percentual de questões dominadas em cada categoria."""

    decorators = [login_obrigatorio]

    def get(self):
        return self.responder(ConsultarProgressoService().executar(request.usuario_id))


class SequenciaController(BaseController):
    """GET /progresso/sequencia — dias seguidos de estudo."""

    decorators = [login_obrigatorio]

    def get(self):
        return self.responder(ConsultarSequenciaService().executar(request.usuario_id))


progresso_bp.add_url_rule("/", view_func=ProgressoController.as_view("progresso_api"), methods=["GET"])
progresso_bp.add_url_rule("/sequencia", view_func=SequenciaController.as_view("sequencia_api"), methods=["GET"])
