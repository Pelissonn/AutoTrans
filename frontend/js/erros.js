// ==========================================
// CADERNO DE ERROS (GET /questoes/erradas)
// ==========================================
async function carregarCadernoErros() {
    const lista = document.getElementById("erros-lista");
    lista.innerHTML = "<p>Carregando...</p>";

    try {
        const erradas = await api.get("/questoes/erradas");

        if (erradas.length === 0) {
            lista.innerHTML = "<p>Nenhuma questão errada por enquanto. Continue assim! 🎉</p>";
            return;
        }

        lista.innerHTML = "";
        erradas.forEach((e) => {
            const q = e.questao;
            const div = document.createElement("div");
            div.className = "card item-questao";
            div.innerHTML = `
                <p class="categoria-tag">${escaparHtml(q.categoria_nome)} — errou ${e.total_erros}x</p>
                <p class="enunciado">${escaparHtml(q.enunciado)}</p>
                ${q.alternativas.map((a) => `<p class="alt ${a.correta ? "alt-certa" : ""}">${a.correta ? "✅" : "▫️"} ${escaparHtml(a.texto)}</p>`).join("")}
            `;
            div.appendChild(criarBotaoFavoritar(q.id));
            lista.appendChild(div);
        });
    } catch (erro) {
        lista.innerHTML = `<p style="color:#e53e3e;">${escaparHtml(erro.message)}</p>`;
    }
}
