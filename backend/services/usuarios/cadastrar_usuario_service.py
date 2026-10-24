from models import Usuario
from repositories import UsuarioRepository


class CadastrarUsuarioService:
    """Caso de uso: o administrador cadastra uma conta manualmente."""

    def __init__(self):
        self.repositorio = UsuarioRepository()

    def executar(self, nome, email, senha, is_admin=False):
        nome = (nome or "").strip()
        email = (email or "").strip().lower()

        if not nome or not email or not senha:
            raise ValueError("Nome, e-mail e senha são obrigatórios.")

        if len(senha) < 4:
            raise ValueError("A senha deve ter pelo menos 4 caracteres.")

        if self.repositorio.buscar_id_por_email(email) is not None:
            raise ValueError("Já existe um usuário cadastrado com este e-mail.")

        usuario = Usuario(nome=nome, email=email, is_admin=bool(is_admin))
        usuario.definir_senha(senha)
        return usuario.salvar().to_dict()
