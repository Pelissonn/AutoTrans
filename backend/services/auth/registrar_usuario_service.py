from models import Usuario
from repositories import UsuarioRepository


class RegistrarUsuarioService:
    """Caso de uso: o aluno cria a própria conta aceitando os termos de uso."""

    def __init__(self):
        self.repositorio = UsuarioRepository()

    def executar(self, nome, email, senha, aceitou_termos):
        nome = (nome or "").strip()
        email = (email or "").strip().lower()

        if not nome or not email or not senha:
            raise ValueError("Nome, e-mail e senha são obrigatórios.")

        if "@" not in email:
            raise ValueError("Informe um e-mail válido.")

        if len(senha) < 4:
            raise ValueError("A senha deve ter pelo menos 4 caracteres.")

        if aceitou_termos is not True:
            raise ValueError("É preciso aceitar os Termos de Uso e a Política de Privacidade.")

        if self.repositorio.buscar_id_por_email(email) is not None:
            raise ValueError("Já existe um usuário cadastrado com este e-mail.")

        usuario = Usuario(nome=nome, email=email)
        usuario.definir_senha(senha)
        usuario.registrar_aceite_termos()

        # O primeiro usuário do sistema vira administrador automaticamente,
        # assim sempre existe alguém que pode gerenciar o conteúdo.
        usuario.is_admin = self.repositorio.contar_usuarios() == 0

        return usuario.salvar()
