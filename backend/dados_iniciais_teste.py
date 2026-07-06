from models import Categoria, Material, Usuario, db


def popular_dados():
    """
    Dados de TESTE para desenvolvimento — usuário, categorias e materiais
    de exemplo. O banco de questões ainda não entra aqui (vem depois, numa
    etapa própria de cadastro de conteúdo).
    """
    if Usuario.query.count() == 0:
        db.session.add(Usuario(nome="Aluno Demo", email="aluno@autotrans.com"))
        db.session.commit()

    if Categoria.query.count() > 0:
        return

    categoria_placas = Categoria(
        nome="Placas de Trânsito",
        descricao="Reconheça placas de regulamentação e advertência.",
    )
    categoria_regras = Categoria(
        nome="Regras de Circulação",
        descricao="Normas básicas do Código de Trânsito Brasileiro.",
    )
    db.session.add_all([categoria_placas, categoria_regras])
    db.session.commit()

    db.session.add(
        Material(
            categoria_id=categoria_placas.id,
            conteudo=(
                "Placas circulares com borda vermelha são de REGULAMENTAÇÃO: indicam "
                "uma obrigação ou proibição (ex.: velocidade máxima). Placas "
                "triangulares amarelas são de ADVERTÊNCIA, alertando sobre um perigo."
            ),
            url="https://www.gov.br/transportes/pt-br/assuntos/transito",
        )
    )
    db.session.add(
        Material(
            categoria_id=categoria_regras.id,
            conteudo=(
                "Em cruzamentos sem sinalização, a prioridade é de quem vem pela "
                "direita do condutor. A distância de segurança entre veículos deve ",
                
                "aumentar conforme a velocidade."
            ),
            url="https://www.gov.br/transportes/pt-br/assuntos/transito",
        )
    )
    db.session.commit()
