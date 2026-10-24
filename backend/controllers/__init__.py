from .auth_controller import auth_bp
from .usuario_controller import usuario_bp
from .categoria_controller import categoria_bp
from .material_controller import material_bp
from .questao_controller import questao_bp
from .alternativa_controller import alternativa_bp
from .simulado_controller import simulado_bp
from .favorito_controller import favorito_bp
from .progresso_controller import progresso_bp
from .ranking_controller import ranking_bp
from .relatorio_controller import relatorio_bp

TODOS_OS_BLUEPRINTS = [
    auth_bp,
    usuario_bp,
    categoria_bp,
    material_bp,
    questao_bp,
    alternativa_bp,
    simulado_bp,
    favorito_bp,
    progresso_bp,
    ranking_bp,
    relatorio_bp,
]

__all__ = ["TODOS_OS_BLUEPRINTS"]
