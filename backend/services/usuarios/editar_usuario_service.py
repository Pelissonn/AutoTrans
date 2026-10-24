from models import Usuario
from repositories import UsuarioRepository
from services.excecoes import RecursoNaoEncontrado


class EditarUsuarioService:
    """Caso de uso: editar nome, e-mail, foto, senha (e, pelo admin, o perfil de acesso)."""

    def __init__(self):
        self.repositorio = UsuarioRepository()

    def executar(self, usuario_id, nome=None, email=None, senha=None, foto_url=None, is_admin=None):
        usuario = Usuario.buscar_por_id(usuario_id)
        if usuario is None:
            raise RecursoNaoEncontrado("Usuário não encontrado.")

        if nome is not None and not nome.strip():
            raise ValueError("O nome não pode ficar em branco.")

        if email:
            email = email.strip().lower()
            outro_id = self.repositorio.buscar_id_por_email(email)
            if outro_id is not None and outro_id != usuario.id:
                raise ValueError("Já existe outro usuário cadastrado com este e-mail.")

        if senha:
            if len(senha) < 4:
                raise ValueError("A senha deve ter pelo menos 4 caracteres.")
            usuario.definir_senha(senha)

        usuario.atualizar(
            nome=nome.strip() if nome else None,
            email=email or None,
            foto_url=foto_url.strip() if foto_url is not None else None,
            is_admin=bool(is_admin) if is_admin is not None else None,
        )
        return usuario.to_dict()
