from models import Resultado, Simulado
from services.excecoes import RecursoNaoEncontrado


class FinalizarSimuladoService:
    """
    Caso de uso: o aluno envia as respostas e o sistema corrige e calcula a nota.

    respostas: [{"item_id": 1, "alternativa_id": 5}, ...]
    """

    def executar(self, simulado_id, respostas, usuario_id_logado):
        simulado = Simulado.buscar_por_id(simulado_id)
        if simulado is None:
            raise RecursoNaoEncontrado("Simulado não encontrado.")

        if not simulado.pertence_a(usuario_id_logado):
            raise PermissionError("Você não tem permissão para finalizar este simulado.")

        # Um simulado só pode ser finalizado uma vez (ex.: clique duplo).
        if simulado.resultado is not None:
            raise ValueError("Este simulado já foi finalizado.")

        if not isinstance(respostas, list):
            raise ValueError("As respostas precisam ser uma lista.")

        escolhas = self._validar_respostas(simulado, respostas)

        for item in simulado.itens:
            item.alternativa_escolhida_id = escolhas.get(item.id)
            item.corrigir()

        # salvar() confirma de uma vez o resultado e a correção dos itens.
        Resultado(simulado_id=simulado.id, nota=simulado.calcular_pontuacao()).salvar()
        return simulado.to_dict()

    def _validar_respostas(self, simulado, respostas):
        """Cada alternativa precisa pertencer à questão daquele item (valida antes de gravar)."""
        itens = {item.id: item for item in simulado.itens}
        escolhas = {}

        for resposta in respostas:
            item = itens.get(resposta.get("item_id")) if isinstance(resposta, dict) else None
            if item is None:
                raise ValueError("Uma das respostas não pertence a este simulado.")

            alternativa_id = resposta.get("alternativa_id")
            if alternativa_id is None:
                continue

            if alternativa_id not in {a.id for a in item.questao.alternativas}:
                raise ValueError("Uma das respostas não é uma alternativa válida da questão.")

            escolhas[item.id] = alternativa_id

        return escolhas
