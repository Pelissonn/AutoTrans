from models import Questao

class ListarQuestoesService:
    def executar(self):
        return Questao.query.all()
    