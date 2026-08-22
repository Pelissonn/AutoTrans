from models import Alternativa


class EditarAlternativaService:
    def executar(self, alternativa_id, texto, correta):
        alternativa = Alternativa.buscar_por_id(alternativa_id)
        if alternativa is None:
            raise ValueError("Alternativa não encontrada.")

        if not texto:
            raise ValueError("O texto da alternativa é obrigatório.")

        alternativa.atualizar(texto=texto, correta=correta)
        return alternativa.to_dict()
