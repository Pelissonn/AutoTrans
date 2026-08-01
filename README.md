# AutoTrans

Aplicação web de estudos para a prova teórica de direção (CNH), no estilo
Duolingo: o aluno escolhe uma categoria, estuda o material e faz simulados
com questões de múltipla escolha.

Projeto escolar desenvolvido em **Flask**, com arquitetura **MVC + Services**.

---

## Tecnologias

- **Python 3** + **Flask** — servidor web e rotas
- **Flask-SQLAlchemy** — ORM (banco SQLite)
- **Jinja2** — templates HTML
- **HTML / CSS / JavaScript** — front-end (SPA por telas, modo escuro, quiz interativo)

---

## Estrutura do projeto

```
AutoTrans/
├── backend/
│   ├── app.py                  → cria e configura a aplicação Flask
│   ├── controllers/            → rotas (Blueprints)
│   │   ├── dashboard_controller.py   → telas principais (/, /inicio, material)
│   │   ├── simulado_controller.py    → fluxo do simulado
│   │   ├── usuario_controller.py     → CRUD de usuários
│   │   ├── categoria_controller.py   → CRUD de categorias
│   │   ├── questao_controller.py     → CRUD de questões
│   │   ├── alternativa_controller.py → CRUD de alternativas
│   │   └── material_controller.py    → CRUD de materiais
│   ├── models/                 → classes do banco de dados
│   │   ├── base.py             → ModeloBase (só o id, herdado por todos)
│   │   ├── usuario.py, categoria.py, material.py, questao.py,
│   │   ├── alternativa.py, simulado.py, item_simulado.py
│   │   └── resultado.py
│   └── services/               → regras de negócio (1 classe por operação CRUD)
│       ├── usuario/  categorias/  questoes/  alternativas/  materiais/
│       └── (create / read / update / delete de cada entidade)
├── frontend/
│   ├── templates/              → páginas HTML (Jinja2)
│   │   ├── bem_vindo.html      → onboarding + login (SPA)
│   │   ├── layout.html         → base com sidebar e modo escuro
│   │   ├── index.html          → painel com telas (trilhas, quiz, ranking...)
│   │   ├── material.html
│   │   ├── simulado/           → responder e resultado
│   │   └── usuario/ categoria/ questao/ alternativa/ material/  → telas de CRUD
│   └── static/
│       ├── css/style.css
│       └── js/script.js
├── requirements.txt
└── README.md
```

---

## Como rodar

1. Clone o repositório:
   ```bash
   git clone https://github.com/Pelissonn/AutoTrans.git
   cd AutoTrans
   ```

2. (Opcional, recomendado) Crie um ambiente virtual:
   ```bash
   python -m venv venv
   venv\Scripts\activate        # Windows
   source venv/bin/activate     # Linux / Mac
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Rode a aplicação:
   ```bash
   cd backend
   python app.py
   ```

5. Abra no navegador: **http://127.0.0.1:5000**

---

## Primeiros passos (banco começa vazio!)

O projeto **não tem mais dados de teste automáticos** — o banco começa zerado.
Antes de usar os simulados, cadastre pelo menos:

1. **1 usuário** → http://127.0.0.1:5000/usuarios/cadastrar
2. **1 categoria** → http://127.0.0.1:5000/categorias/cadastrar
3. **Questões** dessa categoria → http://127.0.0.1:5000/questoes/cadastrar
4. **Alternativas** de cada questão (marcando a correta) → http://127.0.0.1:5000/alternativas/cadastrar

Essas telas também ficam nos links "🛠️ Gerir..." da barra lateral.

---

## Principais rotas

| Rota | O que faz |
|---|---|
| `/` | Tela de boas-vindas / onboarding |
| `/inicio` | Painel principal (trilhas, quiz, ranking, perfil, flashcards) |
| `/categoria/<id>/material` | Material de estudo da categoria |
| `/simulado/categoria/<id>/iniciar` | Cria um simulado com as questões da categoria |
| `/usuarios/`, `/categorias/`, `/questoes/`, `/alternativas/`, `/materiais/` | Telas de gestão (CRUD) |

---

## Próximos passos

- Login de verdade (`Usuario.login()` com sessão)
- Progresso real por categoria nas trilhas
- Conectar o quiz do painel ao banco de questões (hoje usa perguntas fixas no JS)
- Ranking com XP real por usuário
