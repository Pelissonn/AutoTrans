from models import Alternativa, Categoria, Questao
from repositories import CategoriaRepository, QuestaoRepository


class ImportarQuestoesService:
    """
    Caso de uso: importar categorias, questões e alternativas em lote a
    partir de um JSON. Não duplica o que já existe.

    Formato esperado (lista de categorias):
    [
      {
        "categoria": "Legislação de Trânsito",
        "descricao": "Regras de circulação...",
        "questoes": [
          {"enunciado": "...",
           "alternativas": [{"texto": "...", "correta": true}, {"texto": "...", "correta": false}]}
        ]
      }
    ]
    """

    def __init__(self):
        self.categoria_repositorio = CategoriaRepository()
        self.questao_repositorio = QuestaoRepository()

    def executar(self, dados_json):
        if not isinstance(dados_json, list):
            raise ValueError("O JSON precisa ser uma lista de categorias.")

        resumo = {
            "categorias_novas": 0,
            "categorias_reaproveitadas": 0,
            "questoes_novas": 0,
            "questoes_puladas": 0,
            "alternativas_novas": 0,
            "erros": [],
        }

        for indice, item_categoria in enumerate(dados_json, start=1):
            if not isinstance(item_categoria, dict) or not item_categoria.get("categoria"):
                resumo["erros"].append(f"Categoria #{indice}: falta o campo 'categoria' (nome).")
                continue
            self._importar_categoria(item_categoria, resumo)

        return resumo

    def _importar_categoria(self, item_categoria, resumo):
        nome = item_categoria["categoria"].strip()
        categoria_id = self.categoria_repositorio.buscar_id_por_nome(nome)

        if categoria_id is None:
            categoria = Categoria(nome=nome, descricao=item_categoria.get("descricao")).salvar()
            categoria_id = categoria.id
            resumo["categorias_novas"] += 1
        else:
            resumo["categorias_reaproveitadas"] += 1

        for item_questao in item_categoria.get("questoes", []):
            self._importar_questao(item_questao, categoria_id, nome, resumo)

    def _importar_questao(self, item_questao, categoria_id, nome_categoria, resumo):
        enunciado = (item_questao.get("enunciado") or "").strip()
        if not enunciado:
            resumo["erros"].append(f"'{nome_categoria}': uma questão sem enunciado foi ignorada.")
            return

        if self.questao_repositorio.buscar_id_por_enunciado(categoria_id, enunciado) is not None:
            resumo["questoes_puladas"] += 1
            return

        alternativas = item_questao.get("alternativas", [])
        corretas = [a for a in alternativas if a.get("correta")]
        if len(alternativas) < 2 or len(corretas) != 1:
            resumo["erros"].append(
                f"Questão '{enunciado[:40]}...' ignorada: precisa de 2 ou mais alternativas "
                "e exatamente uma correta."
            )
            return

        questao = Questao(categoria_id=categoria_id, enunciado=enunciado).salvar()
        resumo["questoes_novas"] += 1

        for item_alternativa in alternativas:
            Alternativa(
                questao_id=questao.id,
                texto=(item_alternativa.get("texto") or "").strip(),
                correta=bool(item_alternativa.get("correta")),
            ).salvar()
            resumo["alternativas_novas"] += 1
