import os

from flask import Flask

from controllers import dashboard_bp, simulado_bp, usuario_bp, categoria_bp, material_bp, questao_bp, alternativa_bp
from dados_iniciais_teste import popular_dados
from models import db


def criar_app():
    app = Flask(
        __name__,
        template_folder="../frontend/templates",
        static_folder="../frontend/static",
    )

    pasta = os.path.abspath(os.path.dirname(__file__))
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
        pasta, "autotrans.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(simulado_bp)
    app.register_blueprint(usuario_bp)
    app.register_blueprint(categoria_bp)
    app.register_blueprint(material_bp)
    app.register_blueprint(questao_bp)
    app.register_blueprint(alternativa_bp)
    with app.app_context():
        db.create_all()
        popular_dados()

    return app


app = criar_app()

if __name__ == "__main__":
    app.run(debug=True)
