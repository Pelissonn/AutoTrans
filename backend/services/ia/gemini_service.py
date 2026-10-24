import json
import os
import urllib.error
import urllib.request

from services.excecoes import ServicoExternoIndisponivel

URL_GEMINI = "https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent"


class GeminiService:
    """
    Service de integração com a IA (Google Gemini).

    Toda a comunicação HTTP com a API externa fica aqui dentro: nenhum
    Controller ou outro Service sabe a URL, o formato do JSON ou a chave.
    A chave vem da variável de ambiente GEMINI_API_KEY (arquivo .env,
    que não vai para o repositório).
    """

    def __init__(self, chave=None, modelo=None, timeout=45):
        self.chave = chave or os.getenv("GEMINI_API_KEY", "")
        self.modelo = modelo or os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")
        self.timeout = timeout

    def gerar_texto(self, prompt):
        if not self.chave:
            raise ServicoExternoIndisponivel(
                "A explicação por IA não está configurada: defina GEMINI_API_KEY no backend/.env."
            )

        corpo = json.dumps({"contents": [{"parts": [{"text": prompt}]}]}).encode("utf-8")
        requisicao = urllib.request.Request(
            URL_GEMINI.format(modelo=self.modelo),
            data=corpo,
            headers={"Content-Type": "application/json", "x-goog-api-key": self.chave},
            method="POST",
        )

        try:
            with urllib.request.urlopen(requisicao, timeout=self.timeout) as resposta:
                dados = json.loads(resposta.read().decode("utf-8"))
        except (urllib.error.URLError, TimeoutError, ValueError):
            raise ServicoExternoIndisponivel("Não foi possível falar com a IA agora. Tente mais tarde.")

        try:
            partes = dados["candidates"][0]["content"]["parts"]
            return "".join(parte.get("text", "") for parte in partes).strip()
        except (KeyError, IndexError, TypeError):
            raise ServicoExternoIndisponivel("A IA não devolveu uma resposta válida.")
