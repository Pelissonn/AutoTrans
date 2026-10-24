// ==========================================
// PROGRESSO POR CATEGORIA (GET /progresso/)
// e SEQUÊNCIA DE DIAS DE ESTUDO (GET /progresso/sequencia)
// ==========================================

// Devolve um objeto {categoria_id: {percentual, questoes_acertadas, total_questoes}}
async function obterProgressoPorCategoria() {
    const mapa = {};
    try {
        const dados = await api.get("/progresso/");
        dados.categorias.forEach((p) => {
            mapa[p.categoria_id] = p;
        });
    } catch (erro) {
        console.error("Erro ao carregar progresso:", erro);
    }
    return mapa;
}

async function carregarSequencia() {
    const badge = document.getElementById("streak-badge");
    if (!badge) return;

    try {
        const dados = await api.get("/progresso/sequencia");
        const dias = dados.sequencia_atual;
        badge.textContent = `🔥 ${dias} ${dias === 1 ? "dia" : "dias"}`;
        badge.title = `Maior sequência: ${dados.maior_sequencia} | Dias estudados: ${dados.total_dias_estudados}`;
    } catch (erro) {
        badge.textContent = "🔥 0 dias";
    }
}
