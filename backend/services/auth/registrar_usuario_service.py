from models import Usuario


class RegistrarUsuarioService:
    def executar(self, nome, email, senha):
        if not nome or not email or not senha:
            raise ValueError("Nome, e-mail e senha são obrigatórios.")

        if len(senha) < 4:
            raise ValueError("A senha deve ter pelo menos 4 caracteres.")

        usuario_existente = Usuario.buscar_por_email(email)
        if usuario_existente:
            raise ValueError("Já existe um usuário cadastrado com este e-mail.")

        usuario = Usuario(nome=nome, email=email)
        usuario.definir_senha(senha)

        # O primeiro usuário cadastrado no sistema vira administrador
        # automaticamente — assim sempre existe alguém que pode gerenciar
        # categorias/questões/materiais e a lista de usuários, sem precisar
        # mexer direto no banco de dados.
        if Usuario.query.count() == 0:
            usuario.is_admin = True

        usuario.salvar()
        return usuario
