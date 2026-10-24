"""
Popula o banco do AutoTrans com dados de demonstração.

O que é criado:
  - 1 administrador e 5 alunos (com aceite dos termos registrado);
  - 5 categorias com 50 questões reais da prova teórica (questoes_iniciais.json),
    importadas pelo mesmo Service usado na tela de importação;
  - 17 materiais de estudo com links oficiais (materiais_iniciais.json);
  - histórico de simulados finalizados nos últimos dias (alimenta histórico,
    ranking, progresso, sequência de estudo, caderno de erros e relatório);
  - algumas questões favoritas.

Como rodar (a partir da pasta backend):
    python database/popular_banco.py              -> apaga e recria o banco
    python database/popular_banco.py --gerar-sql  -> também gera database/popular_banco.sql

ATENÇÃO: o script APAGA todas as tabelas antes de popular.
"""

import json
import os
import random
import sys
from datetime import datetime, time, timedelta

PASTA_DATABASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(PASTA_DATABASE))  # pasta backend

from app import app  # noqa: E402
from models import (  # noqa: E402
    Favorito,
    ItemSimulado,
    Questao,
    Resultado,
    Simulado,
    Usuario,
    db,
)
from repositories import CategoriaRepository, QuestaoRepository  # noqa: E402
from services.materiais import CadastrarMaterialService  # noqa: E402
from services.questoes import ImportarQuestoesService  # noqa: E402

SENHA_ADMIN = "admin123"
SENHA_ALUNOS = "1234"

# (nome, e-mail, chance de acertar cada questão, quantos simulados, dias atrás do 1º)
ALUNOS = [
    ("Ana Souza", "ana@autotrans.com", 0.90, 9, 8),
    ("Bruno Lima", "bruno@autotrans.com", 0.75, 7, 12),
    ("Carla Mendes", "carla@autotrans.com", 0.65, 6, 10),
    ("Diego Rocha", "diego@autotrans.com", 0.50, 5, 6),
    ("Elisa Martins", "elisa@autotrans.com", 0.80, 4, 3),
]

TABELAS_EM_ORDEM = [
    "usuarios", "categorias", "materiais", "questoes", "alternativas",
    "simulados", "itens_simulado", "resultados", "favoritos",
]


def ler_json(nome_arquivo):
    with open(os.path.join(PASTA_DATABASE, nome_arquivo), encoding="utf-8") as arquivo:
        return json.load(arquivo)


def criar_usuario(nome, email, senha, is_admin=False, dias_atras=30):
    usuario = Usuario(nome=nome, email=email, is_admin=is_admin)
    usuario.definir_senha(senha)
    usuario.registrar_aceite_termos()
    usuario.data_criacao = usuario.data_aceite_termos = datetime.now() - timedelta(days=dias_atras)
    return usuario.salvar()


def criar_conteudo():
    resumo = ImportarQuestoesService().executar(ler_json("questoes_iniciais.json"))
    print(f"Questões importadas: {resumo['questoes_novas']} "
          f"({resumo['alternativas_novas']} alternativas) em {resumo['categorias_novas']} categorias")
    if resumo["erros"]:
        print("Avisos:", *resumo["erros"], sep="\n  ")

    categorias = CategoriaRepository()
    servico_material = CadastrarMaterialService()
    materiais = ler_json("materiais_iniciais.json")
    for material in materiais:
        categoria_id = categorias.buscar_id_por_nome(material["categoria"])
        servico_material.executar(categoria_id, material["conteudo"], material["url"])
    print(f"Materiais cadastrados: {len(materiais)}")


def registrar_simulado(aluno, categoria_id, questoes, chance_acerto, quando, sorteio):
    """Grava um simulado já finalizado em uma data do passado."""
    simulado = Simulado(
        usuario_id=aluno.id,
        categoria_id=categoria_id,
        titulo=f"Simulado - {questoes[0].categoria.nome}",
        data_realizacao=quando,
    ).salvar()

    for questao in questoes:
        correta = questao.alternativa_correta()
        erradas = [a for a in questao.alternativas if not a.correta]
        escolhida = correta if sorteio.random() < chance_acerto else sorteio.choice(erradas)
        item = ItemSimulado(simulado_id=simulado.id, questao=questao, alternativa_escolhida_id=escolhida.id)
        item.corrigir()
        item.salvar()

    Resultado(
        simulado_id=simulado.id,
        nota=simulado.calcular_pontuacao(),
        data_resultado=quando + timedelta(minutes=sorteio.randint(5, 15)),
    ).salvar()


def criar_historico(alunos):
    sorteio = random.Random(2026)  # semente fixa: o resultado é sempre o mesmo
    repositorio = QuestaoRepository()
    categorias = [
        (categoria_id, [Questao.buscar_por_id(i) for i in repositorio.listar_ids_por_categoria(categoria_id)])
        for categoria_id in sorted({q.categoria_id for q in Questao.listar_todos()})
    ]

    total = 0
    hoje = datetime.now().date()
    for aluno, (_, _, chance, quantidade, primeiro_dia) in zip(alunos, ALUNOS):
        # Distribui os simulados do dia mais antigo até hoje (dias seguidos no fim = sequência 🔥).
        dias = sorted({max(0, primeiro_dia - round(i * primeiro_dia / max(1, quantidade - 1)))
                       for i in range(quantidade)}, reverse=True)
        dias += [0] * (quantidade - len(dias))

        for indice, dias_atras in enumerate(dias):
            categoria_id, questoes = categorias[(indice + aluno.id) % len(categorias)]
            sorteadas = sorteio.sample(questoes, min(10, len(questoes)))
            quando = datetime.combine(hoje - timedelta(days=dias_atras), time(sorteio.randint(8, 21), sorteio.randint(0, 59)))
            registrar_simulado(aluno, categoria_id, sorteadas, chance, quando, sorteio)
            total += 1

    print(f"Simulados finalizados criados: {total}")


def criar_favoritos(alunos):
    questoes = Questao.listar_todos()
    sorteio = random.Random(7)
    total = 0
    for aluno in alunos:
        for questao in sorteio.sample(questoes, 3):
            Favorito(usuario_id=aluno.id, questao_id=questao.id).salvar()
            total += 1
    print(f"Favoritos criados: {total}")


def valor_sql(valor):
    if valor is None:
        return "NULL"
    if isinstance(valor, bool):
        return "1" if valor else "0"
    if isinstance(valor, (int, float)):
        return str(valor)
    return "'" + str(valor).replace("'", "''") + "'"


def gerar_arquivo_sql():
    """Exporta os dados como INSERT INTO (útil para carregar o MySQL sem Python)."""
    caminho = os.path.join(PASTA_DATABASE, "popular_banco.sql")
    linhas = [
        "-- Dados de demonstração do AutoTrans (gerado por database/popular_banco.py --gerar-sql)",
        "-- Execute depois de create_database.sql. Senhas: admin123 (admin) e 1234 (alunos).",
        "",
    ]
    for tabela in reversed(TABELAS_EM_ORDEM):
        linhas.append(f"DELETE FROM {tabela};")
    linhas.append("")

    for tabela in TABELAS_EM_ORDEM:
        resultado = db.session.execute(db.text(f"SELECT * FROM {tabela} ORDER BY id"))
        colunas = list(resultado.keys())
        for linha in resultado.all():
            valores = ", ".join(valor_sql(v) for v in linha)
            linhas.append(f"INSERT INTO {tabela} ({', '.join(colunas)}) VALUES ({valores});")
        linhas.append("")

    with open(caminho, "w", encoding="utf-8") as arquivo:
        arquivo.write("\n".join(linhas))
    print(f"Arquivo SQL gerado: {caminho}")


def popular(gerar_sql=False):
    with app.app_context():
        db.drop_all()
        db.create_all()

        criar_usuario("Administrador AutoTrans", "admin@autotrans.com", SENHA_ADMIN, is_admin=True, dias_atras=40)
        alunos = [criar_usuario(nome, email, SENHA_ALUNOS, dias_atras=dias + 5)
                  for nome, email, _, _, dias in ALUNOS]
        print(f"Usuários criados: {len(alunos) + 1} (1 administrador)")

        criar_conteudo()
        criar_historico(alunos)
        criar_favoritos(alunos)

        if gerar_sql:
            gerar_arquivo_sql()

    print("\nBanco populado! Login do administrador: admin@autotrans.com / admin123")
    print("Alunos: ana@, bruno@, carla@, diego@, elisa@autotrans.com / 1234")


if __name__ == "__main__":
    popular(gerar_sql="--gerar-sql" in sys.argv)
