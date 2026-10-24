# Roteiro do vídeo de demonstração — AutoTrans

Duração alvo: **até 5 minutos** (limite da entrega). No fim há uma versão
curta de **2 minutos** (limite da rubrica), com as 4 funcionalidades não-CRUD
exigidas.

## Antes de gravar (checklist)

- [ ] `backend/.env` com `SECRET_KEY` e `GEMINI_API_KEY` preenchidos.
- [ ] Terminal 1: `cd backend` → `python app.py` (API em http://127.0.0.1:5000).
- [ ] Terminal 2: `cd frontend` → `python -m http.server 5500`.
- [ ] Navegador em http://127.0.0.1:5500, **sem estar logado** (se abrir direto o painel, clique em Sair).
- [ ] DevTools aberto na aba **Network (Rede)**, filtro **Fetch/XHR** — mostra que o frontend consome a API.
- [ ] VS Code aberto na pasta do projeto, com `backend/` expandido.
- [ ] Um arquivo `.json` pronto para a importação (pode ser uma cópia reduzida de `backend/database/questoes_iniciais.json` com uma questão nova).

| Perfil | E-mail | Senha |
|---|---|---|
| Administrador | admin@autotrans.com | admin123 |
| Aluna para a demonstração | clarice@autotrans.com | 1234 |
| Outros alunos | artur@, davi@, luanny@, gleison@autotrans.com | 1234 |

---

## Roteiro completo (≈ 5 min)

### Cena 1 — Arquitetura (0:00 – 0:25)
**Tela:** os dois terminais rodando, depois o VS Code.
**Ação:** mostrar a API na porta 5000 e o frontend na 5500; expandir
`controllers/`, `services/`, `models/`, `repositories/`; abrir rapidamente um
repository (ex.: `ranking_repository.py`) mostrando o `SELECT ... GROUP BY`.
**Fala:** "O AutoTrans é uma plataforma de estudo para a prova teórica da CNH.
O frontend e a API rodam em servidores separados. O backend segue as camadas
Controller, Service, Model e Repository, e as consultas especiais dos
repositories são escritas em SQL."

### Cena 2 — Criar conta com termos de uso (0:25 – 0:50)
**Ação:** Começar a Aprender → preencher nome, e-mail novo (ex.:
`video@autotrans.com`) e senha → clicar Continuar **sem** marcar os termos
(aparece o aviso) → marcar "Li e aceito os Termos" (mostrar o link) → Continuar.
**Resultado:** entra no painel. No Network aparece `POST /auth/registro` → 201.
**Fala:** "O cadastro só é concluído com o aceite dos termos, e essa decisão
fica registrada no banco com data e hora."
Depois clicar em **Sair**.

### Cena 3 — Login e painel do aluno (0:50 – 1:05)
**Ação:** Já Tenho Conta → `clarice@autotrans.com` / `1234`.
**Resultado:** painel com "Olá, Clarice" e o selo 🔥 de dias seguidos de estudo.
**Fala:** "A sequência de dias vem de uma consulta no repository que agrupa os
dias em que a aluna finalizou simulados."

### Cena 4 — Trilhas com progresso e simulado (1:05 – 2:00)
**Ação:** Ver Trilhas → mostrar o percentual de questões dominadas em cada
categoria → clicar em uma trilha → responder as 10 questões (errar algumas de
propósito) → Finalizar Simulado.
**Resultado:** tela de resultado com nota, acertos e "Aprovado" ou "Continue estudando".
No Network: `POST /simulados/` e `POST /simulados/<id>/finalizar`.
**Fala:** "O simulado sorteia até 10 questões da categoria. Ao finalizar, o
service corrige cada resposta, calcula a nota e grava o resultado."

### Cena 5 — Histórico, gabarito e explicação por IA (2:00 – 2:45)
**Ação:** Histórico → mostrar média, melhor nota e quantidade → clicar no
simulado que acabou de fazer → Ver gabarito → numa questão errada, clicar
**🤖 Explicar com IA** → clicar **⭐ Favoritar** na mesma questão.
**Resultado:** o gabarito mostra a resposta marcada e a correta; a IA explica
por que a alternativa correta está certa e a marcada está errada.
**Fala:** "A explicação é gerada pelo Google Gemini. A comunicação com a IA
fica isolada em um service próprio, e a chave fica no arquivo .env, fora do
repositório."

### Cena 6 — Caderno de erros, favoritos e busca (2:45 – 3:20)
**Ação:**
1. Caderno de Erros → mostrar as questões mais erradas, com "errou Nx".
2. Favoritas → a questão favoritada aparece → clicar em Remover.
3. Buscar → digitar `placa` → resultados.
**Fala:** "O caderno de erros junta itens, simulados e resultados para listar
as questões que a aluna mais erra. A busca usa LIKE no enunciado."

### Cena 7 — Ranking, materiais e perfil (3:20 – 3:45)
**Ação:** Ranking (pódio e "Sua posição") → Materiais → escolher uma categoria
→ Perfil → mudar o nome → Salvar.
**Fala:** "O ranking ordena os alunos pela média das notas."
Depois **Sair**.

### Cena 8 — Administrador (3:45 – 4:45)
**Ação:** login `admin@autotrans.com` / `admin123` → menu lateral mostra as
opções de administração.
1. **Relatório Geral:** totais, desempenho e taxa de aprovação por categoria,
   questões mais erradas.
2. **Gerir Questões:** cadastrar uma questão → em **Gerir Alternativas**,
   cadastrar duas alternativas (uma correta). Tentar marcar uma segunda como
   correta e mostrar o bloqueio.
3. **Gerir Questões → Importar arquivo:** enviar o `.json` e mostrar o resumo
   (questões novas e puladas).
4. **Gerir Categorias:** tentar excluir uma categoria que já tem simulados e
   mostrar a mensagem de bloqueio.
**Fala:** "As regras de negócio ficam nos services: cada questão tem só uma
alternativa correta, a importação não duplica conteúdo e uma categoria com
simulados não pode ser apagada, para não perder o histórico dos alunos."

### Cena 9 — Encerramento (4:45 – 5:00)
**Ação:** no GitHub, mostrar o README na seção "Funcionalidades Implementadas"
e abrir `docs/diagrama_classes.md`.
**Fala:** "A lista completa das funcionalidades está no README, junto com o
diagrama de classes e os fluxogramas."

---

## Versão curta (≈ 2 min) — 4 funcionalidades não-CRUD

| Tempo | Funcionalidade | O que fazer |
|---|---|---|
| 0:00 – 0:15 | Cliente-servidor | Mostrar os dois terminais (5000 e 5500) e o login da Clarice |
| 0:15 – 0:55 | **1. Simulado com correção automática** | Trilha → responder → Finalizar → nota |
| 0:55 – 1:20 | **2. Gabarito + explicação por IA** | Histórico → simulado → Ver gabarito → 🤖 Explicar com IA |
| 1:20 – 1:35 | **3. Caderno de erros** | Abrir o Caderno de Erros |
| 1:35 – 1:50 | **4. Ranking** | Abrir o Ranking ("Sua posição") |
| 1:50 – 2:00 | Bônus | Mostrar o progresso nas trilhas e o 🔥 de sequência de estudo |

## Dicas de gravação

- Grave em 1080p, com zoom do navegador em 110–125% para o texto ficar legível.
- Se a IA demorar, corte a espera na edição. Ela costuma responder em menos de 5 segundos.
- As funcionalidades mostradas no vídeo precisam ser as mesmas da lista do README.
