const formCategoria = document.querySelector("#form-categoria");
const categoriaIdCampo = document.querySelector("#categoria-id");
const campoNome = document.querySelector("#nome");
const campoDescricao = document.querySelector("#descricao");
const tabelaCategorias = document.querySelector("#tabela-categorias");
const mensagem = document.querySelector("#mensagem");
const tituloFormulario = document.querySelector("#titulo-formulario");
const botaoSalvar = document.querySelector("#botao-salvar");
const botaoCancelar = document.querySelector("#botao-cancelar");

function mostrarMensagem(texto, tipo) {
    mensagem.textContent = texto;
    mensagem.style.color = tipo === "erro" ? "#e53e3e" : "#38a169";
}

function limparFormulario() {
    categoriaIdCampo.value = "";
    campoNome.value = "";
    campoDescricao.value = "";
    tituloFormulario.textContent = "Cadastrar Categoria";
    botaoSalvar.textContent = "Salvar";
}

function renderizarCategorias(categorias) {
    tabelaCategorias.innerHTML = "";
    if (categorias.length === 0) {
        tabelaCategorias.innerHTML = `<tr><td colspan="5">Nenhuma categoria cadastrada.</td></tr>`;
        return;
    }
    categorias.forEach((c) => {
        const linha = document.createElement("tr");
        linha.innerHTML = `
            <td>${c.id}</td><td>${c.nome}</td><td>${c.descricao || ""}</td><td>${c.total_questoes}</td>
            <td>
                <a href="#" onclick='prepararEdicao(${JSON.stringify(c)}); return false;'>Editar</a>
                &nbsp;|&nbsp;
                <a href="#" style="color:#e53e3e;" onclick="deletarCategoria(${c.id}); return false;">Excluir</a>
            </td>`;
        tabelaCategorias.appendChild(linha);
    });
}

async function listarCategorias() {
    try {
        renderizarCategorias(await api.get("/categorias/"));
    } catch (erro) {
        mostrarMensagem(erro.message, "erro");
    }
}

function prepararEdicao(categoria) {
    categoriaIdCampo.value = categoria.id;
    campoNome.value = categoria.nome;
    campoDescricao.value = categoria.descricao || "";
    tituloFormulario.textContent = "Editar Categoria";
    botaoSalvar.textContent = "Atualizar";
}

async function salvarCategoria(evento) {
    evento.preventDefault();
    const dados = { nome: campoNome.value, descricao: campoDescricao.value };
    const id = categoriaIdCampo.value;

    try {
        if (id) {
            await api.put(`/categorias/${id}`, dados);
            mostrarMensagem("Categoria atualizada com sucesso.", "sucesso");
        } else {
            await api.post("/categorias/", dados);
            mostrarMensagem("Categoria cadastrada com sucesso.", "sucesso");
        }
        limparFormulario();
        listarCategorias();
    } catch (erro) {
        mostrarMensagem(erro.message, "erro");
    }
}

async function deletarCategoria(id) {
    if (!confirm("Deseja realmente excluir esta categoria?")) return;
    try {
        await api.delete(`/categorias/${id}`);
        mostrarMensagem("Categoria excluída.", "sucesso");
        listarCategorias();
    } catch (erro) {
        mostrarMensagem(erro.message, "erro");
    }
}

formCategoria.addEventListener("submit", salvarCategoria);
botaoCancelar.addEventListener("click", limparFormulario);
listarCategorias();
