// ==========================================
// GABARITO DE UM SIMULADO (GET /simulados/<id>/gabarito)
// Mostra o que o aluno marcou e qual era a alternativa correta.
// ==========================================
async function verGabarito(simuladoId) {
    const titulo = document.getElementById("gabarito-titulo");
    const conteudo = document.getElementById("gabarito-conteudo");

    titulo.textContent = "Carregando...";
    conteudo.innerHTML = "";
    navigateTo("screen-gabarito");

    try {
        const g = await api.get(`/simulados/${simuladoId}/gabarito`);
        titulo.textContent = `Gabarito — nota ${g.nota}/${g.pontuacao_max}`;

        g.itens.forEach((item, i) => {
            const div = document.createElement("div");
            div.className = "card item-questao";

            let alternativasHtml = "";
            item.alternativas.forEach((alt) => {
                let classe = "";
                let icone = "▫️";
                if (alt.id === item.alternativa_correta_id) {
                    classe = "alt-certa";
                    icone = "✅";
                } else if (alt.id === item.alternativa_escolhida_id) {
                    classe = "alt-errada";
                    icone = "❌";
                }
                const sua = alt.id === item.alternativa_escolhida_id ? " (sua resposta)" : "";
                alternativasHtml += `<p class="alt ${classe}">${icone} ${escaparHtml(alt.texto)}${sua}</p>`;
            });

            div.innerHTML = `
                <p class="categoria-tag">Questão ${i + 1} — ${item.acerto ? "Acertou ✅" : "Errou ❌"}</p>
                <p class="enunciado">${escaparHtml(item.enunciado)}</p>
                ${alternativasHtml}
            `;
            div.appendChild(criarBotaoFavoritar(item.questao_id));
            div.appendChild(criarBotaoExplicarIA(item.questao_id, item.alternativa_escolhida_id));
            conteudo.appendChild(div);
        });
    } catch (erro) {
        titulo.textContent = "Gabarito";
        conteudo.innerHTML = `<p style="color:#e53e3e;">${escaparHtml(erro.message)}</p>`;
    }
}

// ==========================================
// EXPLICAÇÃO COM IA (POST /questoes/<id>/explicacao)
// O backend encaminha o pedido ao Gemini por um Service específico.
// ==========================================
function criarBotaoExplicarIA(questaoId, alternativaEscolhidaId) {
    const caixa = document.createElement("div");
    const btn = document.createElement("button");
    const resposta = document.createElement("p");

    btn.className = "btn-pequeno";
    btn.style.marginLeft = "8px";
    btn.textContent = "🤖 Explicar com IA";
    resposta.className = "explicacao-ia";

    btn.onclick = async () => {
        btn.disabled = true;
        btn.textContent = "🤖 Pensando...";
        try {
            const dados = await api.post(`/questoes/${questaoId}/explicacao`, {
                alternativa_escolhida_id: alternativaEscolhidaId,
            });
            resposta.textContent = dados.explicacao;
            btn.textContent = "🤖 Explicação";
        } catch (erro) {
            resposta.textContent = erro.message;
            resposta.style.color = "#e53e3e";
            btn.disabled = false;
            btn.textContent = "🤖 Explicar com IA";
        }
    };

    caixa.style.display = "inline";
    caixa.appendChild(btn);
    caixa.appendChild(resposta);
    return caixa;
}
