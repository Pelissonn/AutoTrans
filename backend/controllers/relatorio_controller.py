from flask import Blueprint

from controllers.base_controller import BaseController
from services.relatorios import GerarRelatorioGeralService
from utils.auth import admin_obrigatorio

relatorio_bp = Blueprint("relatorio", __name__, url_prefix="/relatorios")


class RelatorioGeralController(BaseController):
    """GET /relatorios/geral — relatório da plataforma (somente administrador)."""

    decorators = [admin_obrigatorio]

    def get(self):
        return self.responder(GerarRelatorioGeralService().executar())


relatorio_bp.add_url_rule("/geral", view_func=RelatorioGeralController.as_view("relatorio_geral"), methods=["GET"])
