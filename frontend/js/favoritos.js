// ==========================================
// FAVORITOS
//   POST   /favoritos/            -> favoritar questão
//   GET    /favoritos/            -> listar questões favoritas
//   DELETE /favoritos/<questao_id> -> remover dos favoritos
// ==========================================

// Botão ⭐ reutilizado nas telas de busca, erros e gabarito.
function criarBotaoFavoritar(questaoId) {
    const btn = document.createElement("button");
    btn.className = "btn-pequeno";
    btn.textContent = "⭐ Favoritar";
    btn.onclick = async () => {
        try {
            await api.post("/favoritos/", { questao_id: questaoId });
            btn.textContent = "⭐ Favoritada";
            btn.disabled = true;
        } catch (erro) {
            // Se já era favorita, só mostramos o estado certo.
            if (erro.message.includes("já está")) {
                btn.textContent = "⭐ Favoritada";
                btn.disabled = true;
            } else {
                alert(erro.message);
            }
        }
    };
    return btn;
}

// Botão ⭐ da tela do simulado (favorita a questão que está na tela).
async function favoritarQuestaoDoQuiz() {
    const aviso = document.getElementById("quiz-mensagem-erro");
    const item = simuladoAtual.itens[indiceQuestaoAtual];
    try {
        await api.post("/favoritos/", { questao_id: item.questao.id });
        aviso.style.color = "#38a169";
        aviso.textContent = "Questão favoritada!";
    } catch (erro) {
        aviso.style.color = "#e53e3e";
        aviso.textContent = erro.message;
    }

    // Volta a cor padrão (vermelho) usada pelas mensagens de erro do simulado.
    setTimeout(() => {
        aviso.textContent = "";
        aviso.style.color = "#e53e3e";
    }, 2000);
}

async function carregarFavoritos() {
    const lista = document.getElementById("favoritos-lista");
    lista.innerHTML = "<p>Carregando favoritos...</p>";

    try {
        const favoritos = await api.get("/favoritos/");

        if (favoritos.length === 0) {
            lista.innerHTML = "<p>Você ainda não favoritou nenhuma questão.</p>";
            return;
        }

        lista.innerHTML = "";
        favoritos.forEach((fav) => {
            const q = fav.questao;
            const div = document.createElement("div");
            div.className = "card item-questao";
            div.innerHTML = `
                <p class="categoria-tag">${escaparHtml(q.categoria_nome)}</p>
                <p class="enunciado">${escaparHtml(q.enunciado)}</p>
                ${q.alternativas.map((a) => `<p class="alt ${a.correta ? "alt-certa" : ""}">${a.correta ? "✅" : "▫️"} ${escaparHtml(a.texto)}</p>`).join("")}
            `;

            const btn = document.createElement("button");
            btn.className = "btn-pequeno btn-remover";
            btn.textContent = "❌ Remover dos favoritos";
            btn.onclick = () => removerFavorito(q.id);
            div.appendChild(btn);

            lista.appendChild(div);
        });
    } catch (erro) {
        lista.innerHTML = `<p style="color:#e53e3e;">${escaparHtml(erro.message)}</p>`;
    }
}

async function removerFavorito(questaoId) {
    try {
        await api.delete(`/favoritos/${questaoId}`);
        carregarFavoritos();
    } catch (erro) {
        alert(erro.message);
    }
}
