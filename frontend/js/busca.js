// ==========================================
// BUSCAR QUESTÕES POR PALAVRA-CHAVE (GET /questoes/buscar?q=...)
// ==========================================
async function buscarQuestoes(evento) {
    evento.preventDefault();

    const palavra = document.getElementById("busca-palavra").value.trim();
    const resultado = document.getElementById("busca-resultado");
    resultado.innerHTML = "<p>Buscando...</p>";

    try {
        const questoes = await api.get(`/questoes/buscar?q=${encodeURIComponent(palavra)}`);

        if (questoes.length === 0) {
            resultado.innerHTML = `<p>Nenhuma questão encontrada para "${escaparHtml(palavra)}".</p>`;
            return;
        }

        resultado.innerHTML = `<p>${questoes.length} questão(ões) encontrada(s):</p>`;
        questoes.forEach((q) => {
            const div = document.createElement("div");
            div.className = "card item-questao";
            div.innerHTML = `
                <p class="categoria-tag">${escaparHtml(q.categoria_nome)}</p>
                <p class="enunciado">${escaparHtml(q.enunciado)}</p>
                ${q.alternativas.map((a) => `<p class="alt ${a.correta ? "alt-certa" : ""}">${a.correta ? "✅" : "▫️"} ${escaparHtml(a.texto)}</p>`).join("")}
            `;
            div.appendChild(criarBotaoFavoritar(q.id));
            resultado.appendChild(div);
        });
    } catch (erro) {
        resultado.innerHTML = `<p style="color:#e53e3e;">${escaparHtml(erro.message)}</p>`;
    }
}

document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("form-busca");
    if (form) form.addEventListener("submit", buscarQuestoes);
});
