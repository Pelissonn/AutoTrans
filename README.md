# AutoTrans

Aplicacao web de estudos para a prova teorica de direcao (CNH), no estilo
Duolingo: o aluno escolhe uma categoria, estuda o material e faz simulados
com questoes de multipla escolha.

Projeto escolar em Flask (API) + HTML/CSS/JS puro (frontend), com
arquitetura Controller -> Service -> Model/Repository -> Banco de Dados.

---

## Funcionalidades Implementadas

1. Cadastro, login e autenticacao de alunos, com senha protegida por hash
   e token de acesso
2. Cadastro de categorias, questoes e alternativas de simulado (banco de
   questoes) - restrito a administradores
3. Cadastro de materiais de estudo, organizados por categoria - restrito
   a administradores
4. Geracao de simulados com correcao automatica, calculando a nota do
   aluno
5. Edicao e exclusao de dados de usuario - restrito a administradores
6. Edicao e exclusao de categorias, questoes e alternativas - restrito a
   administradores
7. Edicao e exclusao de materiais de estudo - restrito a administradores
8. Edicao do proprio perfil pelo usuario logado (nome, foto, senha) e
   exclusao da propria conta (PUT/DELETE /auth/me)
9. Consulta do historico de simulados e estatisticas de evolucao (media,
   melhor e pior nota), usando um Repository para a consulta complexa
   (join Simulado + Resultado)
10. Garantia de que cada aluno so acessa os proprios simulados: ao abrir
    os detalhes de um simulado que nao seja seu (ex.: id manipulado), o
    sistema exibe uma tela de "Acesso negado" em vez dos dados de outro
    usuario (GET /simulados/<id> retorna 403 e o frontend mostra essa
    tela dedicada)

Cada funcionalidade acima esta implementada de ponta a ponta: Interface
-> API Flask -> Controller -> Service -> Model/Repository -> Banco de
Dados.

---

## Tecnologias

- Python 3 + Flask - API REST (so jsonify, sem Jinja/render_template)
- Flask-SQLAlchemy - ORM (banco SQLite)
- Flask-CORS - libera o frontend (outra origem) a chamar a API
- Werkzeug (werkzeug.security) - hash de senha
- itsdangerous - geracao e validacao do token de autenticacao
- HTML / CSS / JavaScript puro - frontend estatico, consome a API via fetch()

---

## Arquitetura

O backend e o frontend sao duas coisas separadas que rodam de forma
independente. O backend nao serve HTML nenhum: so devolve JSON. O
frontend e um conjunto de arquivos estaticos que qualquer navegador abre
direto, e que fala com o backend via fetch().

```
Backend (Flask, porta 5000)  <----  fetch()  ---->  Frontend (arquivos estaticos)
        API JSON                                     HTML + CSS + JS puro
```

### Padrao das camadas (backend)

```
Controller  ->  Service  ->  Model / Repository  ->  Banco de dados
 (rota,         (regra de     Model: CRUD simples
  jsonify)       negocio,     (salvar(), atualizar(), deletar(),
                 validacao)   listar_todos(), buscar_por_id())

                              Repository: consultas especiais
                              (filtros, joins, relatorios, rankings)
```

Regras:
- O Service nunca acessa `db.session` diretamente para CRUD simples. Ele
  chama um metodo da Model (`categoria.salvar()`,
  `Categoria.buscar_por_id(id)` etc.).
- Repository so existe para consultas especiais que nao sao CRUD simples
  (ex.: `HistoricoSimuladoRepository`, que junta Simulado + Resultado e
  calcula estatisticas). Controller e Service nunca fazem essa consulta
  direto - sempre passam pelo Repository.

---

## Autenticacao e permissoes

O login e real: senha com hash (nunca guardada em texto puro), token de
autenticacao, e dois niveis de acesso (aluno comum e administrador).

### Como funciona o login

1. `POST /auth/registro` (nome, email, senha) cria o usuario com a senha
   ja criptografada (werkzeug.security.generate_password_hash) e devolve
   um token.
2. `POST /auth/login` (email, senha) confere a senha
   (check_password_hash) e devolve o mesmo tipo de token.
3. O frontend guarda esse token no localStorage do navegador e manda ele
   no cabecalho `Authorization: Bearer <token>` em toda chamada seguinte
   (isso ja e feito automaticamente pelo js/api.js).
4. Rotas protegidas usam o decorator `@login_obrigatorio` no backend: sem
   um token valido, a API responde 401 Unauthorized.

Por que token em vez de cookie/sessao do Flask: o frontend roda em uma
origem separada do backend (Live Server em uma porta, API em outra), e
cookies entre origens diferentes em localhost sao inconsistentes entre
navegadores.

### Aluno x Administrador

- O **primeiro usuario cadastrado** no sistema vira administrador
  automaticamente (`is_admin = True`), garantindo que sempre exista
  alguem que possa gerenciar o banco de questoes e os usuarios sem
  precisar mexer direto no banco de dados.
- Cadastrar/editar/excluir categorias, questoes, alternativas, materiais
  e usuarios exige administrador - protegido pelo decorator
  `@admin_obrigatorio` no backend (retorna 403 para quem nao e admin).
  As telas `admin_*.html` tambem verificam isso no frontend
  (`js/admin-guard.js`) e redirecionam quem nao e admin, mas a protecao
  de verdade e sempre a do backend.
- Listar/ver categorias, questoes, alternativas e materiais continua
  publico para qualquer aluno logado (precisa ver as trilhas e o
  conteudo de estudo).
- Ninguem consegue se autopromover a administrador editando o proprio
  perfil (`PUT /auth/me` ignora o campo `is_admin` do corpo da
  requisicao) - so um administrador pode tornar outro usuario admin,
  pela tela de gestao de usuarios.

### Perfil e seguranca por usuario

- `GET /auth/me` e `PUT /auth/me` sempre agem sobre o usuario dono do
  token - nunca sobre um id vindo da URL ou do corpo da requisicao,
  entao ninguem consegue ver ou editar a conta de outra pessoa por essa
  rota.
- `DELETE /auth/me` exclui a propria conta do usuario logado.
- Cada simulado so pode ser visto/finalizado pelo proprio usuario dono
  dele - se o token for de outro usuario, a API responde 403 Forbidden e
  o frontend mostra uma tela de "Acesso negado".

---

## Estrutura do projeto

```
AutoTrans/
|-- backend/
|   |-- app.py                       -> cria a API Flask + CORS (sem Jinja)
|   |-- auth_utils.py                -> token (login_obrigatorio) e permissao (admin_obrigatorio)
|   |-- seed_questoes_reais.py       -> popula categorias/questoes/alternativas reais
|   |-- seed_materiais_reais.py      -> popula materiais de estudo (com links oficiais)
|   |-- requirements.txt
|   |-- controllers/                 -> rotas (Blueprints), so devolvem JSON
|   |   |-- auth_controller.py            -> registro, login, logout, me (GET/PUT/DELETE)
|   |   |-- usuario_controller.py         -> CRUD restrito a admin
|   |   |-- categoria_controller.py       -> leitura publica, escrita restrita a admin
|   |   |-- questao_controller.py         -> leitura publica, escrita restrita a admin
|   |   |-- alternativa_controller.py     -> leitura publica, escrita restrita a admin
|   |   |-- material_controller.py        -> leitura publica, escrita restrita a admin
|   |   `-- simulado_controller.py        -> inclui /simulados/historico
|   |-- models/                      -> CRUD "Active Record" (1 arquivo por entidade)
|   |   |-- base.py                  -> ModeloBase (so o id)
|   |   |-- usuario.py               -> senha_hash, foto_url, is_admin
|   |   |-- categoria.py, material.py, questao.py,
|   |   |-- alternativa.py, simulado.py, item_simulado.py, resultado.py
|   |-- services/                    -> 1 pasta por entidade, 1 classe por operacao
|   |   |-- auth/  usuario/  categorias/  questoes/  alternativas/  materiais/
|   |   `-- simulados/  (inclui consultar_historico_service.py)
|   `-- repositories/                -> consultas especiais (joins, relatorios)
|       `-- historico_simulado_repository.py
|-- frontend/
|   |-- index.html                   -> tela de boas-vindas / onboarding / login / cadastro
|   |-- css/style.css
|   |-- js/
|   |   |-- api.js                    -> configuracao central da API + fetch() + token
|   |   |-- script.js                 -> navegacao entre telas (SPA), modo escuro
|   |   |-- auth.js                   -> cadastro/login reais
|   |   |-- admin-guard.js            -> bloqueia telas admin_*.html para quem nao e admin
|   |   |-- painel.js                 -> trilhas, quiz, historico, perfil (dados reais da API)
|   |   |-- materiais.js
|   |   `-- admin_*.js                -> 1 arquivo por CRUD de administracao
|   `-- paginas/
|       |-- painel.html               -> painel principal (trilhas, quiz, perfil, historico...)
|       |-- materiais.html
|       `-- admin_usuarios.html, admin_categorias.html, admin_questoes.html,
|           admin_alternativas.html, admin_materiais.html
|-- requirements.txt
`-- README.md
```

---

## Como rodar

### 1. Backend (API)

```bash
git clone https://github.com/Pelissonn/AutoTrans.git
cd AutoTrans
pip install -r requirements.txt
cd backend
python app.py
```

A API sobe em http://127.0.0.1:5000. Teste abrindo esse link no navegador
- deve aparecer um JSON com a lista de rotas disponiveis.

Importante: se voce ja tinha um banco criado antes de uma mudanca no
schema (novo campo, nova tabela), apague `backend/autotrans.db` antes de
rodar de novo - o SQLite nao adiciona colunas automaticamente.

### 2. Popular o banco com conteudo real

O banco comeca vazio. Rode os dois scripts abaixo (nessa ordem) para
cadastrar categorias, questoes, alternativas e materiais de estudo reais:

```bash
cd backend
python seed_questoes_reais.py
python seed_materiais_reais.py
```

Rodar os scripts de novo nao duplica nada - eles pulam o que ja existe.

### 3. Frontend (arquivos estaticos)

O frontend nao precisa do Flask para rodar - e so abrir os arquivos .html
da pasta frontend/ no navegador. Recomendado usar a extensao Live Server
do VS Code:

1. Clique com o botao direito em frontend/index.html
2. Escolha "Open with Live Server"
3. O navegador abre em um endereco proprio (ex.: http://127.0.0.1:5500),
   diferente da porta do backend

Importante: o backend precisa estar rodando (passo 1) para o frontend
funcionar. O frontend nunca deve ser acessado pela porta 5000 - essa
porta e exclusiva da API.

Atencao (Live Server): se o VS Code estiver com a pasta inteira do
projeto aberta (backend + frontend juntos), o Live Server pode recarregar
a pagina sozinho toda vez que o arquivo `backend/autotrans.db` mudar. O
arquivo `.vscode/settings.json` do projeto ja configura o Live Server
para ignorar a pasta `backend/` - reabra o VS Code depois de clonar para
essa configuracao valer.

### 4. Criar uma conta e testar

1. Abra o frontend, clique em "Comecar a Aprender" e crie uma conta - a
   **primeira conta criada vira administrador automaticamente**
2. Como administrador, cadastre categorias/questoes/materiais pelas telas
   "Gerir ..." (ou use os scripts de seed do passo 2)
3. Crie uma segunda conta (aluno comum) para testar o fluxo de estudo sem
   acesso as telas de administracao
4. Escolha uma trilha (categoria) e inicie um simulado
5. Responda todas as questoes e finalize - a nota aparece na tela de
   resultado, e o simulado passa a contar em "Meu Historico"

---

## Principais rotas da API

| Metodo | Rota | O que faz | Acesso |
|---|---|---|---|
| POST | /auth/registro | Cria conta {nome, email, senha} | Publico |
| POST | /auth/login | Login {email, senha} | Publico |
| POST | /auth/logout | Encerra a sessao (no cliente) | Publico |
| GET | /auth/me | Dados do usuario logado | Logado |
| PUT | /auth/me | Edita os proprios dados {nome, email, senha, foto_url} | Logado |
| DELETE | /auth/me | Exclui a propria conta | Logado |
| GET | /categorias/ , /categorias/<id> | Lista/busca categorias | Publico |
| POST / PUT / DELETE | /categorias/ , /categorias/<id> | Cadastra/edita/remove categoria | Admin |
| GET | /questoes/ , /questoes/<id> | Lista/busca questoes (aceita ?categoria_id=) | Publico |
| POST / PUT / DELETE | /questoes/ , /questoes/<id> | Cadastra/edita/remove questao | Admin |
| GET | /alternativas/ , /alternativas/<id> | Lista/busca alternativas (aceita ?questao_id=) | Publico |
| POST / PUT / DELETE | /alternativas/ , /alternativas/<id> | Cadastra/edita/remove alternativa | Admin |
| GET | /materiais/ , /materiais/<id> | Lista/busca materiais (aceita ?categoria_id=) | Publico |
| POST / PUT / DELETE | /materiais/ , /materiais/<id> | Cadastra/edita/remove material | Admin |
| GET | /usuarios/ | Lista usuarios | Admin |
| POST / PUT / DELETE | /usuarios/ , /usuarios/<id> | Cadastra/edita/remove usuario | Admin |
| POST | /simulados/ | Inicia simulado {categoria_id} (usuario vem do token) | Logado |
| GET | /simulados/<id> | Busca um simulado (so o dono ve; senao 403) | Logado |
| POST | /simulados/<id>/finalizar | Envia respostas e gera o resultado (so o dono) | Logado |
| GET | /simulados/historico | Lista simulados do usuario logado + estatisticas | Logado |

---

## Modelagem (models)

| Model | Campos principais | Observacao |
|---|---|---|
| Usuario | nome, email, senha_hash, foto_url, is_admin, data_criacao, data_atualizacao | senha nunca fica em texto puro |
| Categoria | nome, descricao | agrupa questoes e materiais |
| Material | categoria_id, conteudo, url | pertence a uma categoria |
| Questao | categoria_id, enunciado | pertence a uma categoria |
| Alternativa | questao_id, texto, correta | pertence a uma questao |
| Simulado | usuario_id, categoria_id, titulo, pontuacao_max, data_realizacao | criado ao iniciar um simulado |
| ItemSimulado | simulado_id, questao_id, alternativa_escolhida_id, acerto | uma linha por questao respondida |
| Resultado | simulado_id, nota, data_resultado | gerado ao finalizar o simulado |

Todos os models herdam de ModeloBase, que define apenas o campo id. Cada
model que precisa de data de criacao declara a propria coluna com o nome
que faz sentido para ele (ex.: Simulado.data_realizacao,
Resultado.data_resultado).

---

## Proximos passos

- Progresso real por categoria nas trilhas
- Ranking real com XP por usuario
- Justificativa da resposta apos a correcao automatica
- Conectar o quiz do painel principal ao banco de questoes real via API
