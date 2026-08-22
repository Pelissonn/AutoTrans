from models import Usuario


class CadastrarUsuarioService:
    """Usado pela tela de administração para criar contas manualmente."""

    def executar(self, nome, email, senha, is_admin=False):
        if not nome or not email or not senha:
            raise ValueError("Nome, e-mail e senha são obrigatórios.")

        usuario_existente = Usuario.buscar_por_email(email)
        if usuario_existente:
            raise ValueError("Já existe um usuário cadastrado com este e-mail.")

        usuario = Usuario(nome=nome, email=email, is_admin=bool(is_admin))
        usuario.definir_senha(senha)
        usuario.salvar()
        return usuario.to_dict()
