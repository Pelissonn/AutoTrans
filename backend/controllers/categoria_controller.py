from flask import Blueprint

from controllers.base_controller import ERROS_DE_NEGOCIO, BaseController
from services.categorias import (
    BuscarCategoriaService,
    CadastrarCategoriaService,
    EditarCategoriaService,
    ExcluirCategoriaService,
    ListarCategoriasService,
)
from utils.auth import admin_obrigatorio

categoria_bp = Blueprint("categoria", __name__, url_prefix="/categorias")


class CategoriaController(BaseController):
    """Categorias (trilhas): leitura pública, escrita só administrador."""

    def get(self, id=None):
        if id is None:
            return self.responder(ListarCategoriasService().executar())
        try:
            return self.responder(BuscarCategoriaService().executar(id))
        except ERROS_DE_NEGOCIO as erro:
            return self.responder_erro(erro)

    @admin_obrigatorio
    def post(self):
        dados = self.dados_json()
        try:
            categoria = CadastrarCategoriaService().executar(dados.get("nome"), dados.get("descricao"))
            return self.responder(categoria, 201)
        except ERROS_DE_NEGOCIO as erro:
            return self.responder_erro(erro)

    @admin_obrigatorio
    def put(self, id):
        dados = self.dados_json()
        try:
            categoria = EditarCategoriaService().executar(id, dados.get("nome"), dados.get("descricao"))
            return self.responder(categoria)
        except ERROS_DE_NEGOCIO as erro:
            return self.responder_erro(erro)

    @admin_obrigatorio
    def delete(self, id):
        try:
            return self.responder(ExcluirCategoriaService().executar(id))
        except ERROS_DE_NEGOCIO as erro:
            return self.responder_erro(erro)


CategoriaController.registrar_crud(categoria_bp, "categoria_api")
