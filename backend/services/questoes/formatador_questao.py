from repositories import AlternativaRepository


def anexar_alternativas(linhas_questoes):
    """
    Recebe linhas de questões vindas de um Repository (dicionários) e
    acrescenta a lista de alternativas de cada uma, no mesmo formato que
    Questao.to_dict() devolve. Usado pelos Services de busca, caderno de
    erros, favoritos e filtro por categoria.
    """
    repositorio = AlternativaRepository()
    for linha in linhas_questoes:
        linha["alternativas"] = repositorio.listar_por_questao(linha["id"])
    return linhas_questoes
