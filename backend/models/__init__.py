from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Cada import abaixo registra a tabela da entidade no SQLAlchemy (usado pelo create_all).
from .base import ModeloBase
from .usuario import Usuario
from .categoria import Categoria
from .material import Material
from .questao import Questao
from .alternativa import Alternativa
from .simulado import Simulado
from .item_simulado import ItemSimulado
from .resultado import Resultado
from .favorito import Favorito

__all__ = [
    "db",
    "ModeloBase",
    "Usuario",
    "Categoria",
    "Material",
    "Questao",
    "Alternativa",
    "Simulado",
    "ItemSimulado",
    "Resultado",
    "Favorito",
]
