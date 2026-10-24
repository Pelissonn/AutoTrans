// Registros da tabela por id: o botão Editar busca aqui (evita colocar JSON dentro do HTML).
const registrosPorId = {};

const formQuestao = document.querySelector("#form-questao");
const questaoIdCampo = document.querySelector("#questao-id");
const campoEnunciado = document.querySelector("#enunciado");
const campoCategoria = document.querySelector("#categoria_id");
const tabelaQuestoes = document.querySelector("#tabela-questoes");
const mensagem = document.querySelector("#mensagem");
const tituloFormulario = document.querySelector("#titulo-formulario");
const botaoSalvar = document.querySelector("#botao-salvar");
const botaoCancelar = document.querySelector("#botao-cancelar");

function mostrarMensagem(texto, tipo) {
    mensagem.textContent = texto;
    mensagem.style.color = tipo === "erro" ? "#e53e3e" : "#38a169";
}

function limparFormulario() {
    questaoIdCampo.value = "";
    campoEnunciado.value = "";
    tituloFormulario.textContent = "Cadastrar Questão";
    botaoSalvar.textContent = "Salvar";
}

async function carregarCategoriasNoSelect() {
    const categorias = await api.get("/categorias/");
    campoCategoria.innerHTML = categorias
        .map((c) => `<option value="${c.id}">${c.nome}</option>`)
        .join("");
}

function renderizarQuestoes(questoes) {
    tabelaQuestoes.innerHTML = "";
    if (questoes.length === 0) {
        tabelaQuestoes.innerHTML = `<tr><td colspan="4">Nenhuma questão cadastrada.</td></tr>`;
        return;
    }
    questoes.forEach((q) => {
        const linha = document.createElement("tr");
        registrosPorId[q.id] = q;
        linha.innerHTML = `
            <td>${q.id}</td><td>${escaparHtml(q.enunciado)}</td><td>${escaparHtml(q.categoria_nome || "—")}</td>
            <td>
                <a href="#" onclick="prepararEdicao(registrosPorId[${q.id}]); return false;">Editar</a>
                &nbsp;|&nbsp;
                <a href="#" style="color:#e53e3e;" onclick="deletarQuestao(${q.id}); return false;">Excluir</a>
            </td>`;
        tabelaQuestoes.appendChild(linha);
    });
}

async function listarQuestoes() {
    try {
        renderizarQuestoes(await api.get("/questoes/"));
    } catch (erro) {
        mostrarMensagem(erro.message, "erro");
    }
}

function prepararEdicao(questao) {
    questaoIdCampo.value = questao.id;
    campoEnunciado.value = questao.enunciado;
    campoCategoria.value = questao.categoria_id;
    tituloFormulario.textContent = "Editar Questão";
    botaoSalvar.textContent = "Atualizar";
}

async function salvarQuestao(evento) {
    evento.preventDefault();
    const dados = { enunciado: campoEnunciado.value, categoria_id: campoCategoria.value };
    const id = questaoIdCampo.value;

    try {
        if (id) {
            await api.put(`/questoes/${id}`, dados);
            mostrarMensagem("Questão atualizada com sucesso.", "sucesso");
        } else {
            await api.post("/questoes/", dados);
            mostrarMensagem("Questão cadastrada com sucesso.", "sucesso");
        }
        limparFormulario();
        listarQuestoes();
    } catch (erro) {
        mostrarMensagem(erro.message, "erro");
    }
}

async function deletarQuestao(id) {
    if (!confirm("Deseja realmente excluir esta questão? As alternativas dela também serão apagadas.")) return;
    try {
        await api.delete(`/questoes/${id}`);
        mostrarMensagem("Questão excluída.", "sucesso");
        listarQuestoes();
    } catch (erro) {
        mostrarMensagem(erro.message, "erro");
    }
}

// ==========================================
// IMPORTAR QUESTÕES EM LOTE (POST /questoes/importar)
// ==========================================
const campoArquivo = document.querySelector("#arquivo-importacao");
const botaoImportar = document.querySelector("#botao-importar");
const divResultadoImportacao = document.querySelector("#resultado-importacao");

async function importarArquivo() {
    divResultadoImportacao.innerHTML = "";

    const arquivo = campoArquivo.files[0];
    if (!arquivo) {
        divResultadoImportacao.innerHTML = `<p style="color:#e53e3e;">Escolha um arquivo .json primeiro.</p>`;
        return;
    }

    let dados;
    try {
        dados = JSON.parse(await arquivo.text());
    } catch (erro) {
        divResultadoImportacao.innerHTML = `<p style="color:#e53e3e;">Arquivo inválido: ${escaparHtml(erro.message)}</p>`;
        return;
    }

    try {
        const resumo = await api.post("/questoes/importar", dados);
        let html = `
            <p style="color:#38a169; font-weight:600;">Importação concluída.</p>
            <ul>
                <li>Categorias novas: ${resumo.categorias_novas}</li>
                <li>Categorias reaproveitadas: ${resumo.categorias_reaproveitadas}</li>
                <li>Questões novas: ${resumo.questoes_novas}</li>
                <li>Questões já existentes (puladas): ${resumo.questoes_puladas}</li>
                <li>Alternativas novas: ${resumo.alternativas_novas}</li>
            </ul>`;
        if (resumo.erros.length > 0) {
            html += `<p style="color:#e53e3e; font-weight:600;">Avisos:</p><ul>`;
            resumo.erros.forEach((aviso) => { html += `<li style="color:#e53e3e;">${escaparHtml(aviso)}</li>`; });
            html += `</ul>`;
        }
        divResultadoImportacao.innerHTML = html;
        await carregarCategoriasNoSelect();
        await listarQuestoes();
    } catch (erro) {
        divResultadoImportacao.innerHTML = `<p style="color:#e53e3e;">${escaparHtml(erro.message)}</p>`;
    }
}

formQuestao.addEventListener("submit", salvarQuestao);
botaoCancelar.addEventListener("click", limparFormulario);
botaoImportar.addEventListener("click", importarArquivo);

(async () => {
    await carregarCategoriasNoSelect();
    await listarQuestoes();
})();
