import os
import secrets
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_cors import CORS
from sqlalchemy.exc import SQLAlchemyError

from controllers import TODOS_OS_BLUEPRINTS
from models import db

PASTA_BACKEND = Path(__file__).resolve().parent


def carregar_chave_secreta():
    """
    Chave que assina os tokens de login, lida do .env (SECRET_KEY). Se não
    estiver configurada, usa uma chave aleatória só para esta execução.
    """
    chave = os.getenv("SECRET_KEY", "")
    if not chave or chave == "troque-por-uma-chave-aleatoria":
        print("AVISO: SECRET_KEY não configurada no backend/.env. "
              "Usando uma chave temporária (os logins expiram ao reiniciar).")
        return secrets.token_urlsafe(32)
    return chave


def endereco_do_banco():
    """SQLite em backend/instance/autotrans.db por padrão; MySQL se DATABASE_URL existir."""
    url_configurada = os.getenv("DATABASE_URL")
    if url_configurada:
        return url_configurada

    arquivo_sqlite = PASTA_BACKEND / "instance" / "autotrans.db"
    arquivo_sqlite.parent.mkdir(exist_ok=True)
    return f"sqlite:///{arquivo_sqlite.as_posix()}"


def criar_app():
    load_dotenv(PASTA_BACKEND / ".env")

    app = Flask(__name__)
    CORS(app)  # o frontend roda em outro servidor (porta 5500)

    app.config["SQLALCHEMY_DATABASE_URI"] = endereco_do_banco()
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = carregar_chave_secreta()
    app.json.ensure_ascii = False

    db.init_app(app)

    for blueprint in TODOS_OS_BLUEPRINTS:
        app.register_blueprint(blueprint)

    # Tratamento central de erro de banco: a transação é desfeita e a API
    # responde 500. Assim nenhum Controller precisa conhecer o db.session.
    @app.errorhandler(SQLAlchemyError)
    def erro_de_banco(erro):
        db.session.rollback()
        return jsonify({"erro": "Erro ao acessar o banco de dados."}), 500

    @app.get("/")
    def home():
        return jsonify({
            "mensagem": "API do AutoTrans funcionando.",
            "rotas": {
                "auth": "POST /auth/registro, POST /auth/login, GET|PUT|DELETE /auth/me",
                "usuarios": "/usuarios/ (admin)",
                "categorias": "/categorias/",
                "materiais": "/materiais/?categoria_id=<id>",
                "questoes": "/questoes/?categoria_id=<id>, /questoes/buscar?q=, /questoes/erradas",
                "importar_questoes": "POST /questoes/importar (admin)",
                "explicacao_ia": "POST /questoes/<id>/explicacao",
                "alternativas": "/alternativas/?questao_id=<id>",
                "simulados": "POST /simulados/, GET /simulados/<id>, POST /simulados/<id>/finalizar",
                "historico": "GET /simulados/historico",
                "gabarito": "GET /simulados/<id>/gabarito",
                "favoritos": "/favoritos/",
                "progresso": "GET /progresso/, GET /progresso/sequencia",
                "ranking": "GET /ranking/",
                "relatorio": "GET /relatorios/geral (admin)",
            },
        })

    with app.app_context():
        # Cria as tabelas que ainda não existem (facilita os testes em sala).
        db.create_all()

    return app


app = criar_app()

if __name__ == "__main__":
    debug = os.getenv("FLASK_DEBUG", "True") == "True"
    app.run(debug=debug, host="0.0.0.0", port=5000)
