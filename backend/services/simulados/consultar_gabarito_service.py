from models import Simulado
from services.excecoes import RecursoNaoEncontrado


class ConsultarGabaritoService:
    """Caso de uso: gabarito do simulado — o que o aluno marcou e qual era a correta."""

    def executar(self, simulado_id, usuario_id_logado):
        simulado = Simulado.buscar_por_id(simulado_id)
        if simulado is None:
            raise RecursoNaoEncontrado("Simulado não encontrado.")

        if not simulado.pertence_a(usuario_id_logado):
            raise PermissionError("Você não tem permissão para ver este simulado.")

        if simulado.resultado is None:
            raise ValueError("Finalize o simulado para ver o gabarito.")

        itens = []
        for item in simulado.itens:
            correta = item.questao.alternativa_correta()
            itens.append({
                "item_id": item.id,
                "questao_id": item.questao.id,
                "enunciado": item.questao.enunciado,
                "alternativas": [a.to_dict() for a in item.questao.alternativas],
                "alternativa_escolhida_id": item.alternativa_escolhida_id,
                "alternativa_correta_id": correta.id if correta else None,
                "acerto": item.acerto,
            })

        return {
            "simulado_id": simulado.id,
            "titulo": simulado.titulo,
            "nota": simulado.resultado.nota,
            "pontuacao_max": simulado.pontuacao_max,
            "aprovado": simulado.resultado.aprovado(simulado.pontuacao_max),
            "itens": itens,
        }
