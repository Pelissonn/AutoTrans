from .base_repository import BaseRepository


class UsuarioRepository(BaseRepository):
    """Consultas especiais sobre usuários."""

    def contar_usuarios(self):
        """Quantos usuários existem (o primeiro cadastro vira administrador)."""
        return self._buscar_valor("SELECT COUNT(*) FROM usuarios")

    def buscar_id_por_email(self, email):
        """Filtro específico: localiza o id do usuário pelo e-mail (login/cadastro)."""
        linha = self._buscar_um(
            "SELECT id FROM usuarios WHERE LOWER(email) = LOWER(:email)",
            {"email": email},
        )
        return linha["id"] if linha else None
