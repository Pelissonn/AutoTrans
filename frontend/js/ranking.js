// ==========================================
// RANKING DE ALUNOS (GET /ranking/)
// ==========================================
async function carregarRanking() {
    const lista = document.getElementById("ranking-lista");
    const minhaPosicao = document.getElementById("ranking-minha-posicao");
    lista.innerHTML = "<p>Carregando ranking...</p>";
    minhaPosicao.textContent = "";

    try {
        const dados = await api.get("/ranking/");

        if (dados.ranking.length === 0) {
            lista.innerHTML = "<p>Ainda ninguém finalizou um simulado. Seja o primeiro!</p>";
            return;
        }

        const classes = ["gold", "silver", "bronze"];
        const medalhas = ["🥇", "🥈", "🥉"];

        lista.innerHTML = "";
        dados.ranking.forEach((aluno, i) => {
            const div = document.createElement("div");
            div.className = "ranking-item " + (classes[i] || "");
            div.innerHTML = `
                <span class="rank-pos">${medalhas[i] || aluno.posicao + "º"}</span>
                <span style="flex:1; text-align:left;">${escaparHtml(aluno.nome)}</span>
                <span class="rank-xp">Média ${aluno.media} (${aluno.total_simulados} simulados)</span>
            `;
            lista.appendChild(div);
        });

        if (dados.minha_posicao) {
            minhaPosicao.textContent = `Sua posição: ${dados.minha_posicao}º de ${dados.total_participantes}`;
        } else {
            minhaPosicao.textContent = "Finalize um simulado para entrar no ranking.";
        }
    } catch (erro) {
        lista.innerHTML = `<p style="color:#e53e3e;">${escaparHtml(erro.message)}</p>`;
    }
}
