from models import db, Alternativa

class DeletarAlternativaService:
    def executar(self, alternativa_id):
        alternativa = Alternativa.query.get(alternativa_id)
        if not alternativa:
            raise ValueError("Alternativa não encontrada.")
        db.session.delete(alternativa)
        db.session.commit()