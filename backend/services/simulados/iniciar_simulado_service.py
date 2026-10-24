import random

from models import Categoria, ItemSimulado, Questao, Simulado
from repositories import QuestaoRepository
from services.excecoes import RecursoNaoEncontrado

QUESTOES_POR_SIMULADO = 10


class IniciarSimuladoService:
    """
    Caso de uso: o aluno inicia um simulado de uma categoria. São sorteadas
    até 10 questões válidas (com alternativa correta cadastrada).
    """

    def __init__(self):
        self.repositorio = QuestaoRepository()

    def executar(self, usuario_id, categoria_id):
        if not categoria_id:
            raise ValueError("Informe a categoria do simulado.")

        categoria = Categoria.buscar_por_id(categoria_id)
        if categoria is None:
            raise RecursoNaoEncontrado("Categoria não encontrada.")

        questoes = [Questao.buscar_por_id(i) for i in self.repositorio.listar_ids_por_categoria(categoria.id)]
        validas = [q for q in questoes if len(q.alternativas) >= 2 and q.alternativa_correta()]
        if not validas:
            raise ValueError("Esta categoria ainda não tem questões prontas para simulado.")

        sorteadas = random.sample(validas, min(QUESTOES_POR_SIMULADO, len(validas)))

        simulado = Simulado(
            usuario_id=usuario_id,
            categoria_id=categoria.id,
            titulo=f"Simulado - {categoria.nome}",
        ).salvar()

        for questao in sorteadas:
            ItemSimulado(simulado_id=simulado.id, questao_id=questao.id).salvar()

        return simulado.to_dict()
