"""
Erros de regra de negócio lançados pelos Services.

O Controller só traduz cada tipo de erro para o status HTTP certo:
  - ValueError                 -> 400 (dados inválidos / regra violada)
  - RecursoNaoEncontrado       -> 404
  - PermissionError            -> 403 (o recurso é de outro usuário)
  - ServicoExternoIndisponivel -> 503 (IA/API externa fora do ar ou sem chave)
"""


class RecursoNaoEncontrado(ValueError):
    pass


class ServicoExternoIndisponivel(RuntimeError):
    pass
