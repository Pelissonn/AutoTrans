from flask import Blueprint, redirect, render_template, request, url_for

from models import Categoria, ItemSimulado, Resultado, Simulado, Usuario, db

simulado_bp = Blueprint("simulado", __name__, url_prefix="/simulado")


@simulado_bp.route("/categoria/<int:categoria_id>/iniciar")
def iniciar(categoria_id):
    categoria = Categoria.query.get(categoria_id)
    usuario = Usuario.obter_padrao()

    simulado = Simulado(
        usuario_id=usuario.id,
        categoria_id=categoria.id,
        titulo=f"Simulado - {categoria.nome}",
    )
    db.session.add(simulado)
    db.session.commit()

    for questao in categoria.questoes:
        db.session.add(ItemSimulado(simulado_id=simulado.id, questao_id=questao.id))
    db.session.commit()

    return redirect(url_for("simulado.responder", simulado_id=simulado.id))


@simulado_bp.route("/<int:simulado_id>")
def responder(simulado_id):
    simulado = Simulado.buscar_por_id(simulado_id)
    return render_template("simulado/responder.html", simulado=simulado)


@simulado_bp.route("/<int:simulado_id>/finalizar", methods=["POST"])
def finalizar(simulado_id):
    simulado = Simulado.buscar_por_id(simulado_id)

    for item in simulado.itens:
        alternativa_id = request.form.get(f"item_{item.id}")
        if alternativa_id:
            item.alternativa_escolhida_id = int(alternativa_id)
        item.verificar()
    db.session.commit()

    resultado = Resultado(simulado_id=simulado.id, nota=simulado.calcular_pontuacao())
    db.session.add(resultado)
    db.session.commit()

    return redirect(url_for("simulado.resultado", simulado_id=simulado.id))


@simulado_bp.route("/<int:simulado_id>/resultado")
def resultado(simulado_id):
    simulado = Simulado.buscar_por_id(simulado_id)
    resultado = Resultado.buscar_por_simulado(simulado_id)
    aprovado = resultado.nota >= simulado.pontuacao_max * 0.7
    return render_template(
        "simulado/resultado.html", simulado=simulado, resultado=resultado, aprovado=aprovado
    )
