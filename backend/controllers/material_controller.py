from flask import Blueprint, request

from controllers.base_controller import ERROS_DE_NEGOCIO, BaseController
from services.materiais import (
    BuscarMaterialService,
    CadastrarMaterialService,
    EditarMaterialService,
    ExcluirMaterialService,
    ListarMateriaisPorCategoriaService,
    ListarMateriaisService,
)
from utils.auth import admin_obrigatorio

material_bp = Blueprint("material", __name__, url_prefix="/materiais")


class MaterialController(BaseController):
    """Materiais de estudo: leitura pública (com filtro ?categoria_id=), escrita só administrador."""

    def get(self, id=None):
        try:
            if id is not None:
                return self.responder(BuscarMaterialService().executar(id))

            categoria_id = request.args.get("categoria_id", type=int)
            if categoria_id:
                return self.responder(ListarMateriaisPorCategoriaService().executar(categoria_id))
            return self.responder(ListarMateriaisService().executar())
        except ERROS_DE_NEGOCIO as erro:
            return self.responder_erro(erro)

    @admin_obrigatorio
    def post(self):
        dados = self.dados_json()
        try:
            material = CadastrarMaterialService().executar(
                dados.get("categoria_id"), dados.get("conteudo"), dados.get("url")
            )
            return self.responder(material, 201)
        except ERROS_DE_NEGOCIO as erro:
            return self.responder_erro(erro)

    @admin_obrigatorio
    def put(self, id):
        dados = self.dados_json()
        try:
            material = EditarMaterialService().executar(
                id, dados.get("conteudo"), dados.get("url"), dados.get("categoria_id")
            )
            return self.responder(material)
        except ERROS_DE_NEGOCIO as erro:
            return self.responder_erro(erro)

    @admin_obrigatorio
    def delete(self, id):
        try:
            return self.responder(ExcluirMaterialService().executar(id))
        except ERROS_DE_NEGOCIO as erro:
            return self.responder_erro(erro)


MaterialController.registrar_crud(material_bp, "material_api")
