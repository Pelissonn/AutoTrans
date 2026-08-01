import os

from flask import Flask

from controllers import (
    alternativa_bp,
    categoria_bp,
    dashboard_bp,
    material_bp,
    questao_bp,
    simulado_bp,
    usuario_bp,
)
from models import db


def criar_app():
    pasta = os.path.abspath(os.path.dirname(__file__))
    raiz = os.path.abspath(os.path.join(pasta, ".."))

    app = Flask(
        __name__,
        template_folder=os.path.join(raiz, "frontend", "templates"),
        static_folder=os.path.join(raiz, "frontend", "static"),
    )

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(pasta, "autotrans.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "autotrans-dev"

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

    return app


app = criar_app()

if __name__ == "__main__":
    app.run(debug=True)
