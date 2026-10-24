from models import Usuario
from repositories import UsuarioRepository


class LoginService:
    """Caso de uso: autenticar o usuário pelo e-mail e senha."""

    def __init__(self):
        self.repositorio = UsuarioRepository()

    def executar(self, email, senha):
        email = (email or "").strip().lower()
        if not email or not senha:
            raise ValueError("E-mail e senha são obrigatórios.")

        usuario_id = self.repositorio.buscar_id_por_email(email)
        usuario = Usuario.buscar_por_id(usuario_id) if usuario_id else None

        # Mensagem genérica de propósito: não revela se o e-mail existe.
        if usuario is None or not usuario.verificar_senha(senha):
            raise ValueError("E-mail ou senha inválidos.")

        return usuario
