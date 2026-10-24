# AutoTrans

Plataforma web de estudos para a prova teórica da CNH, no estilo Duolingo:
o aluno estuda o material de cada categoria, faz simulados com correção
automática, acompanha a própria evolução e compete no ranking.

Projeto em **Flask (API REST)** + **HTML/CSS/JavaScript puro (frontend)**,
com arquitetura em camadas:

```
Interface/Tela → API Flask → Controller → Service → Model / Repository → Banco de Dados
```

---

## Descrição, público-alvo e problema resolvido

**Descrição.** O AutoTrans reúne o conteúdo de estudo da prova teórica da CNH
organizado por categoria (Legislação, Sinalização, Direção Defensiva,
Primeiros Socorros e Mecânica Básica), um banco de questões de múltipla
escolha e simulados que corrigem as respostas na hora, guardam o histórico
e mostram o progresso do aluno. Administradores mantêm o conteúdo e
acompanham um relatório geral da plataforma.

**Público-alvo.** Candidatos à primeira habilitação (e quem precisa refazer a
prova teórica), principalmente jovens que estudam pelo computador ou celular.

**Problema resolvido.** O estudo costuma ser feito com apostilas longas e
simulados soltos, sem correção imediata nem acompanhamento. O AutoTrans
oferece estudo por categoria, simulados com nota automática, gabarito
comentado (inclusive por IA), caderno de erros e um histórico que mostra se o
aluno está melhorando.

---

## Casos de uso principais (com telas)

| # | Caso de uso | Tela | Endpoint | Caminho pelas camadas |
|---|---|---|---|---|
| 1 | Fazer um simulado com correção automática | `painel.html` (Trilhas → Quiz → Resultado) | `POST /simulados/`, `POST /simulados/<id>/finalizar` | `SimuladoController` → `IniciarSimuladoService` (usa `QuestaoRepository`) / `FinalizarSimuladoService` → Models `Simulado`, `ItemSimulado`, `Resultado` |
| 2 | Consultar histórico e estatísticas | `painel.html` (Meu Histórico) | `GET /simulados/historico` | `HistoricoSimuladoController` → `ConsultarHistoricoService` → `SimuladoRepository` (SQL com JOIN e AVG/MAX/MIN) |
| 3 | Ranking dos alunos | `painel.html` (Ranking) | `GET /ranking/` | `RankingController` → `ConsultarRankingService` → `RankingRepository` (SQL com GROUP BY) |
| 4 | Caderno de erros | `painel.html` (Caderno de Erros) | `GET /questoes/erradas` | `CadernoErrosController` → `ListarQuestoesErradasService` → `QuestaoRepository` |
| 5 | Relatório geral (administrador) | `admin_relatorio.html` | `GET /relatorios/geral` | `RelatorioGeralController` → `GerarRelatorioGeralService` → `RelatorioRepository` |

Fluxogramas desses casos de uso (passo a passo pelas camadas, incluindo o
Repository): [`docs/fluxogramas.md`](docs/fluxogramas.md).
Roteiro do vídeo de demonstração: [`docs/roteiro_video.md`](docs/roteiro_video.md).

---

## Funcionalidades Implementadas

Todas estão implementadas de ponta a ponta (Tela → API Flask → Controller →
Service → Model/Repository → Banco de Dados).

**Conta e acesso**

1. Criar conta de aluno com aceite dos Termos de Uso (decisão registrada no banco)
2. Fazer login (senha com hash e token de acesso)
3. Visualizar o próprio perfil
4. Editar o próprio perfil (nome, foto e senha)
5. Excluir a própria conta (apaga também o histórico)

**Estudo e simulados**

6. Iniciar simulado por categoria (sorteio de até 10 questões)
7. Finalizar simulado com correção automática e cálculo da nota
8. Consultar histórico de simulados com estatísticas (média, melhor e pior nota)
9. Ver os detalhes de um simulado (bloqueado para simulados de outro aluno)
10. Ver o gabarito do simulado (resposta marcada × correta)
11. Explicar uma questão com Inteligência Artificial (Google Gemini)
12. Estudar os materiais de uma categoria
13. Buscar questões por palavra-chave
14. Caderno de erros (questões que o aluno mais errou)
15. Favoritar questão
16. Listar questões favoritas
17. Remover questão dos favoritos
18. Progresso por categoria (% de questões dominadas em cada trilha)
19. Sequência de dias de estudo (🔥 streak)
20. Ranking dos alunos pela média das notas

**Administração** (somente administrador)

21. Relatório geral da plataforma (totais, desempenho e aprovação por categoria, questões mais erradas)
22. Cadastrar usuário
23. Listar usuários
24. Editar usuário (inclusive tornar administrador)
25. Excluir usuário
26. Cadastrar categoria
27. Listar categorias
28. Editar categoria
29. Excluir categoria (bloqueada se já houver simulados nela)
30. Cadastrar questão
31. Listar questões (com filtro por categoria)
32. Editar questão
33. Excluir questão (bloqueada se já foi respondida em simulado)
34. Cadastrar alternativa (cada questão aceita só uma correta)
35. Listar alternativas (com filtro por questão)
36. Editar alternativa
37. Excluir alternativa (bloqueada se já foi escolhida em simulado)
38. Cadastrar material de estudo
39. Listar materiais (com filtro por categoria)
40. Editar material
41. Excluir material
42. Importar questões, alternativas e categorias em lote por arquivo JSON (não duplica)

---

## Arquitetura

O backend e o frontend são **duas aplicações separadas**, executadas em
servidores diferentes. O backend não serve HTML: só devolve JSON. O frontend
é um conjunto de arquivos estáticos que fala com a API apenas por `fetch`
(`frontend/js/api.js`).

```
  Frontend (porta 5500)                       Backend / API (porta 5000)
  HTML + CSS + JavaScript   --- fetch --->    Flask → Controller → Service → Model/Repository → SQLite/MySQL
  python -m http.server 5500                  python app.py
```

### Camadas do backend

- **Controllers** (`backend/controllers/`): classes (`flask.views.MethodView`)
  ligadas a um recurso (`CategoriaController`, `QuestaoController`,
  `SimuladoController`...). Recebem a requisição, leem os dados, chamam o
  Service e devolvem o JSON com o status HTTP. Não têm regra de negócio.
  Todas herdam de `BaseController`, que traduz os erros dos Services em
  400/403/404/503.
- **Services** (`backend/services/`): **uma classe por caso de uso, um arquivo
  por classe** (ex.: `CadastrarQuestaoService`, `FinalizarSimuladoService`,
  `ConsultarRankingService`). Validam os dados e coordenam o caso de uso
  chamando Models e Repositories. A integração com a IA fica isolada no
  `services/ia/gemini_service.py`.
- **Models** (`backend/models/`): entidades do domínio. Herdam de
  `ModeloBase` (`db.Model`), que concentra o CRUD com ORM: `salvar()`,
  `atualizar()`, `deletar()`, `listar_todos()` e `buscar_por_id()`.
- **Repositories** (`backend/repositories/`): consultas especiais **escritas
  em SQL** (`SELECT`, `JOIN`, `GROUP BY`, `COUNT/AVG/MAX/MIN`, `LIKE`), com
  parâmetros nomeados (`:usuario_id`) para evitar SQL Injection. Não repetem o
  CRUD simples das Models. Controller e Service nunca escrevem SQL.

| Repository | Consultas (SQL) | Usado por |
|---|---|---|
| `UsuarioRepository` | contar usuários; localizar usuário pelo e-mail | `RegistrarUsuarioService`, `LoginService`, `CadastrarUsuarioService`, `EditarUsuarioService` |
| `CategoriaRepository` | localizar categoria pelo nome; contar simulados da categoria | cadastro/edição/exclusão de categoria, importação |
| `QuestaoRepository` | filtro por categoria; busca por palavra (`LIKE`); caderno de erros (`JOIN` + `GROUP BY`); contar respostas | busca, caderno de erros, simulado, exclusão, importação |
| `AlternativaRepository` | filtro por questão; contar respostas; contar corretas da questão | alternativas e montagem das questões |
| `MaterialRepository` | materiais de uma categoria (`JOIN`) | `ListarMateriaisPorCategoriaService` |
| `SimuladoRepository` | histórico do aluno (`JOIN` simulados + resultados + categorias); estatísticas (`AVG/MAX/MIN`) | `ConsultarHistoricoService` |
| `FavoritoRepository` | questões favoritas do aluno; localizar favorito | favoritos |
| `RankingRepository` | ranking (`AVG` por aluno, `ORDER BY`) | `ConsultarRankingService` |
| `ProgressoRepository` | questões distintas acertadas por categoria; dias de estudo (`DISTINCT DATE`) | progresso e sequência |
| `RelatorioRepository` | totais, desempenho por categoria, questões mais erradas | `GerarRelatorioGeralService` |

### Estrutura de diretórios

```
AutoTrans/
├── backend/
│   ├── app.py                    → cria a API Flask, CORS e registra os blueprints
│   ├── .env.example              → modelo das variáveis de ambiente (SECRET_KEY, GEMINI_API_KEY...)
│   ├── controllers/              → base_controller + 1 arquivo por recurso
│   ├── services/                 → 1 pasta por recurso, 1 arquivo por caso de uso
│   │   ├── auth/  usuarios/  categorias/  materiais/  questoes/  alternativas/
│   │   ├── simulados/  favoritos/  progresso/  ranking/  relatorios/
│   │   ├── ia/gemini_service.py  → integração com a IA (API externa)
│   │   └── excecoes.py           → erros de negócio (404, 503)
│   ├── models/                   → base (CRUD) + 9 entidades
│   ├── repositories/             → base_repository + 10 repositories com SQL
│   ├── utils/                    → auth.py (token, login/admin obrigatório), datas.py
│   ├── database/
│   │   ├── create_database.sql   → tabelas para MySQL
│   │   ├── popular_banco.py      → popula o banco com dados de demonstração
│   │   ├── popular_banco.sql     → os mesmos dados em INSERT INTO (MySQL)
│   │   ├── questoes_iniciais.json, materiais_iniciais.json
│   └── instance/autotrans.db     → banco SQLite já populado
├── frontend/
│   ├── index.html                → boas-vindas, criar conta (com termos) e login
│   ├── css/style.css
│   ├── js/                       → api.js, auth.js, painel.js, gabarito.js, ranking.js, ...
│   └── paginas/                  → painel, materiais, termos e admin_*
├── README.md                     → este arquivo (único README do projeto)
├── docs/
│   ├── diagrama_classes.md (.mmd) → diagrama de classes do domínio
│   ├── fluxogramas.md             → fluxogramas dos casos de uso
│   └── roteiro_video.md           → roteiro do vídeo de demonstração
└── requirements.txt
```

---

## Diagrama de classes

O diagrama de classes do domínio (Models, atributos, herança, composição e
agregação) está em [`docs/diagrama_classes.md`](docs/diagrama_classes.md)
(fonte Mermaid em [`docs/diagrama_classes.mmd`](docs/diagrama_classes.mmd)).
O GitHub renderiza o diagrama direto na página.

---

## Tecnologias

- Python 3 + Flask: API REST (somente JSON)
- Flask-SQLAlchemy: CRUD com ORM nas Models; conexão usada pelos Repositories para executar SQL escrito à mão
- SQLite (padrão) ou MySQL (PyMySQL)
- Flask-CORS: o frontend (porta 5500) chama a API (porta 5000)
- Werkzeug: hash de senha · itsdangerous: token de acesso · python-dotenv: `.env`
- Google Gemini (API REST): explicação das questões por IA
- HTML, CSS e JavaScript puro no frontend (`fetch`)

---

## Como rodar

São dois processos, cada um em um terminal.

### 1. Backend (API)

```bash
pip install -r requirements.txt
cd backend
copy .env.example .env        # Linux/Mac: cp .env.example .env
python app.py
```

Edite o `backend/.env`: coloque uma chave em `SECRET_KEY`
(`python -c "import secrets; print(secrets.token_urlsafe(32))"`) e, para a
explicação por IA, a sua `GEMINI_API_KEY`
([Google AI Studio](https://aistudio.google.com/)). Sem a chave do Gemini,
todo o resto funciona e o botão de IA avisa que ela não está configurada.
O modelo usado é definido em `GEMINI_MODEL` (padrão: `gemini-3.5-flash-lite`).
O arquivo `.env` nunca vai para o GitHub (está no `.gitignore`); só o
`.env.example`, sem chaves, fica no repositório.

A API sobe em http://127.0.0.1:5000.

### 2. Frontend (outro terminal)

```bash
cd frontend
python -m http.server 5500
```

Abra http://127.0.0.1:5500 (ou use o Live Server do VS Code).

### 3. Banco de dados

O banco `backend/instance/autotrans.db` **já vem populado**. Para recriá-lo do zero:

```bash
cd backend
python database/popular_banco.py
```

Isso cria 6 usuários, 5 categorias, 50 questões (200 alternativas), 17
materiais com links oficiais, 31 simulados finalizados nos últimos dias
(alimentam histórico, ranking, progresso, sequência, caderno de erros e
relatório) e 15 favoritos. Com `--gerar-sql` o script também gera
`database/popular_banco.sql`.

Logins do banco que está no repositório:

| Perfil | E-mail | Senha |
|---|---|---|
| Administrador | admin@autotrans.com | admin123 |
| Alunos | artur@, davi@, clarice@, luanny@, gleison@autotrans.com | 1234 |

(Se o banco for recriado pelo `popular_banco.py`, os alunos passam a ser
ana@, bruno@, carla@, diego@ e elisa@autotrans.com, também com a senha 1234.)

**MySQL (opcional):** execute `database/create_database.sql` e depois
`database/popular_banco.sql`; no `.env`, descomente
`DATABASE_URL=mysql+pymysql://root:sua_senha@localhost:3306/autotrans_db`.
O SQL dos Repositories é padrão e funciona nos dois bancos.

### 4. Importação de questões em lote

Na tela **Gerir Questões** (administrador) é possível enviar um arquivo `.json`
com categorias, questões e alternativas. O arquivo
`backend/database/questoes_iniciais.json` está no formato esperado e serve de modelo:

```json
[
  {
    "categoria": "Legislação de Trânsito",
    "descricao": "Regras de circulação...",
    "questoes": [
      {"enunciado": "...",
       "alternativas": [{"texto": "...", "correta": true}, {"texto": "...", "correta": false}]}
    ]
  }
]
```

Categorias e questões que já existem são reaproveitadas (não duplicam).

---

## Autenticação, permissões e privacidade

- `POST /auth/registro` e `POST /auth/login` devolvem um token assinado; o
  frontend o envia em `Authorization: Bearer <token>`.
- Senhas só como hash. Chaves (`SECRET_KEY`, `GEMINI_API_KEY`) só no `.env`, fora do repositório.
- `@login_obrigatorio` (401) e `@admin_obrigatorio` (403) protegem as rotas.
- `/auth/me`, simulados e favoritos sempre usam o usuário do token — ninguém
  acessa dados de outro aluno; ninguém se promove a administrador pelo perfil.
- **Termo de consentimento:** o cadastro exige aceitar os Termos de Uso
  (`frontend/paginas/termos.html`); o aceite e a data ficam gravados em
  `usuarios.aceitou_termos` e `usuarios.data_aceite_termos`.

---

## Principais rotas da API

| Método | Rota | O que faz | Acesso |
|---|---|---|---|
| POST | /auth/registro | Cria conta {nome, email, senha, aceitou_termos} | Público |
| POST | /auth/login | Login {email, senha} | Público |
| GET / PUT / DELETE | /auth/me | Ver, editar e excluir a própria conta | Logado |
| GET | /categorias/ , /categorias/<id> | Lista e consulta categorias | Público |
| GET | /questoes/?categoria_id= , /questoes/<id> | Lista/filtra e consulta questões | Público |
| GET | /questoes/buscar?q= | Busca por palavra-chave | Público |
| GET | /questoes/erradas | Caderno de erros | Logado |
| POST | /questoes/<id>/explicacao | Explicação por IA | Logado |
| POST | /questoes/importar | Importação em lote (JSON) | Admin |
| GET | /alternativas/?questao_id= | Lista/filtra alternativas | Público |
| GET | /materiais/?categoria_id= | Lista/filtra materiais | Público |
| POST / PUT / DELETE | /categorias, /questoes, /alternativas, /materiais | Cadastro, edição e exclusão | Admin |
| GET / POST / PUT / DELETE | /usuarios/ , /usuarios/<id> | Gestão de usuários | Admin |
| POST | /simulados/ | Inicia simulado {categoria_id} | Logado |
| GET | /simulados/<id> | Detalhes (só o dono) | Logado |
| POST | /simulados/<id>/finalizar | Corrige e gera a nota | Logado |
| GET | /simulados/<id>/gabarito | Gabarito | Logado |
| GET | /simulados/historico | Histórico e estatísticas | Logado |
| GET / POST / DELETE | /favoritos/ , /favoritos/<questao_id> | Favoritos do aluno | Logado |
| GET | /progresso/ , /progresso/sequencia | Progresso e sequência de estudo | Logado |
| GET | /ranking/ | Ranking dos alunos | Logado |
| GET | /relatorios/geral | Relatório geral | Admin |

---

## SOLID no AutoTrans

| Princípio | Como aparece no código |
|---|---|
| Responsabilidade única | `FinalizarSimuladoService` só corrige e dá a nota; `RankingRepository` só monta a consulta do ranking; `RankingController` só recebe a requisição e devolve o JSON. |
| Aberto/fechado | Para criar a explicação por IA foi adicionada a classe `ExplicarQuestaoService`, sem alterar nenhum service que já existia. |
| Substituição de Liskov | `Questao`, `Usuario`, `Simulado` e as demais entidades podem ser usadas por qualquer service através dos métodos herdados de `ModeloBase`. |
| Segregação de interfaces | Os controllers só implementam os verbos HTTP de que precisam: `RelatorioGeralController` tem apenas `get`, `RegistroController` tem apenas `post`. |
| Inversão de dependência | `ExplicarQuestaoService(ia=...)` recebe o serviço de IA pronto; trocar o Gemini por outro provedor não muda o caso de uso. |
