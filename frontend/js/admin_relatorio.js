// ==========================================
// RELATÓRIO GERAL (GET /relatorios/geral) — só administrador
// ==========================================
async function carregarRelatorio() {
    const totais = document.querySelector("#relatorio-totais");
    const tabelaCategorias = document.querySelector("#tabela-categorias");
    const tabelaErradas = document.querySelector("#tabela-erradas");
    const mensagem = document.querySelector("#mensagem");

    try {
        const r = await api.get("/relatorios/geral");

        totais.innerHTML = `
            <div class="stat-box"><span class="stat-value">${r.totais.usuarios}</span><span class="stat-label">Usuários</span></div>
            <div class="stat-box"><span class="stat-value">${r.totais.questoes}</span><span class="stat-label">Questões</span></div>
            <div class="stat-box"><span class="stat-value">${r.totais.simulados_finalizados}</span><span class="stat-label">Simulados</span></div>
            <div class="stat-box"><span class="stat-value">${r.totais.media_geral}</span><span class="stat-label">Média geral</span></div>
        `;

        tabelaCategorias.innerHTML = "";
        if (r.por_categoria.length === 0) {
            tabelaCategorias.innerHTML = `<tr><td colspan="4">Nenhum simulado finalizado ainda.</td></tr>`;
        }
        r.por_categoria.forEach((c) => {
            const linha = document.createElement("tr");
            linha.innerHTML = `<td>${escaparHtml(c.categoria_nome)}</td><td>${c.simulados}</td><td>${c.media}</td><td>${c.taxa_aprovacao}%</td>`;
            tabelaCategorias.appendChild(linha);
        });

        tabelaErradas.innerHTML = "";
        if (r.questoes_mais_erradas.length === 0) {
            tabelaErradas.innerHTML = `<tr><td colspan="3">Nenhum erro registrado ainda.</td></tr>`;
        }
        r.questoes_mais_erradas.forEach((q) => {
            const linha = document.createElement("tr");
            linha.innerHTML = `<td>${escaparHtml(q.enunciado)}</td><td>${escaparHtml(q.categoria_nome)}</td><td>${q.erros}</td>`;
            tabelaErradas.appendChild(linha);
        });
    } catch (erro) {
        mensagem.style.color = "#e53e3e";
        mensagem.textContent = erro.message;
    }
}

document.addEventListener("DOMContentLoaded", carregarRelatorio);
