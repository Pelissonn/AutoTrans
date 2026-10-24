"""
Autenticação baseada em token assinado (sem sessão/cookie).

O frontend roda em uma origem separada do backend (porta 5500 x 5000), e
cookies entre origens diferentes são inconsistentes entre navegadores. Um
token no cabeçalho Authorization evita esse problema.
"""

from functools import wraps

from flask import current_app, jsonify, request
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer

TOKEN_VALIDADE_SEGUNDOS = 60 * 60 * 24 * 7  # 7 dias


def _serializer():
    """A chave vem de app.config["SECRET_KEY"], carregada do .env no app.py."""
    return URLSafeTimedSerializer(current_app.config["SECRET_KEY"])


def gerar_token(usuario_id):
    """Cria um token assinado contendo o id do usuário."""
    return _serializer().dumps({"usuario_id": usuario_id})


def obter_usuario_id_do_token():
    """Lê 'Authorization: Bearer <token>' e devolve o usuario_id, ou None."""
    cabecalho = request.headers.get("Authorization", "")
    if not cabecalho.startswith("Bearer "):
        return None

    token = cabecalho[len("Bearer "):].strip()
    try:
        dados = _serializer().loads(token, max_age=TOKEN_VALIDADE_SEGUNDOS)
    except (BadSignature, SignatureExpired):
        return None

    return dados.get("usuario_id")


def _usuario_do_token():
    # Import local para evitar import circular (models -> utils -> models).
    from models import Usuario

    usuario_id = obter_usuario_id_do_token()
    if usuario_id is None:
        return None
    return Usuario.buscar_por_id(usuario_id)


def login_obrigatorio(funcao_view):
    """
    Só executa a view se houver um token válido de um usuário existente.
    Disponibiliza o id do usuário logado em request.usuario_id.
    """

    @wraps(funcao_view)
    def wrapper(*args, **kwargs):
        usuario = _usuario_do_token()
        if usuario is None:
            return jsonify({"erro": "Autenticação necessária. Faça login novamente."}), 401

        request.usuario_id = usuario.id
        return funcao_view(*args, **kwargs)

    return wrapper


def admin_obrigatorio(funcao_view):
    """Exige token válido E que o usuário logado seja administrador."""

    @wraps(funcao_view)
    def wrapper(*args, **kwargs):
        usuario = _usuario_do_token()
        if usuario is None:
            return jsonify({"erro": "Autenticação necessária. Faça login novamente."}), 401

        if not usuario.is_admin:
            return jsonify({"erro": "Apenas administradores podem realizar esta ação."}), 403

        request.usuario_id = usuario.id
        return funcao_view(*args, **kwargs)

    return wrapper
