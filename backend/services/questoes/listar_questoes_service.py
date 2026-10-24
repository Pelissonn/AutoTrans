from models import Questao


class ListarQuestoesService:
    """Caso de uso: listar todas as questões com suas alternativas."""

    def executar(self):
        return [questao.to_dict() for questao in Questao.listar_todos()]
