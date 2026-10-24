from models import Usuario
from services.excecoes import RecursoNaoEncontrado


class ExcluirUsuarioService:
    """Caso de uso: excluir uma conta (apaga também o histórico do aluno)."""

    def executar(self, usuario_id):
        usuario = Usuario.buscar_por_id(usuario_id)
        if usuario is None:
            raise RecursoNaoEncontrado("Usuário não encontrado.")

        usuario.deletar()
        return {"mensagem": "Usuário excluído com sucesso."}
