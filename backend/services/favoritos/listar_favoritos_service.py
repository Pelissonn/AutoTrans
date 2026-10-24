from repositories import FavoritoRepository
from services.questoes.formatador_questao import anexar_alternativas
from utils.datas import para_texto_iso


class ListarFavoritosService:
    """Caso de uso: listar as questões favoritas do aluno logado."""

    def __init__(self):
        self.repositorio = FavoritoRepository()

    def executar(self, usuario_id):
        linhas = anexar_alternativas(self.repositorio.listar_questoes_favoritas(usuario_id))

        return [
            {
                "id": linha.pop("favorito_id"),
                "data_criacao": para_texto_iso(linha.pop("data_criacao")),
                "questao_id": linha["id"],
                "questao": linha,
            }
            for linha in linhas
        ]
