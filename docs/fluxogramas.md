# Fluxogramas dos casos de uso

Cada fluxograma mostra o passo a passo pelas camadas:
**Tela → API Flask → Controller → Service → Model / Repository → Banco de dados**.

---

## 1. Recuperação de dados — Consultar o ranking dos alunos

Tela `painel.html` (aba 🏆 Ranking) → `GET /ranking/`

```mermaid
flowchart TD
    A["Tela: aluno abre a aba Ranking<br/>(frontend/js/ranking.js)"] -->|"fetch GET /ranking/<br/>Authorization: Bearer token"| B["API Flask<br/>ranking_bp"]
    B --> C{"login_obrigatorio<br/>token válido?"}
    C -->|não| C1["401 - Faça login novamente"] --> Z
    C -->|sim| D["RankingController.get()<br/>lê request.usuario_id"]
    D --> E["ConsultarRankingService.executar(usuario_id)"]
    E --> F["RankingRepository.listar_ranking()"]
    F --> G[("Banco<br/>SELECT u.id, u.nome, AVG(r.nota), MAX(r.nota), COUNT(r.id)<br/>FROM usuarios JOIN simulados JOIN resultados<br/>GROUP BY u.id ORDER BY media DESC")]
    G --> H["Service numera as posições,<br/>arredonda as médias e acha a posição do aluno logado"]
    H --> I["Controller devolve JSON 200<br/>{ranking, minha_posicao, total_participantes}"]
    I --> Z["Tela mostra o pódio 🥇🥈🥉 e 'Sua posição'"]
```

## 2. Recuperação de dados — Consultar o histórico de simulados

Tela `painel.html` (aba 📊 Meu Histórico) → `GET /simulados/historico`

```mermaid
flowchart TD
    A["Tela: aluno abre Meu Histórico<br/>(frontend/js/painel.js)"] -->|"fetch GET /simulados/historico"| B["HistoricoSimuladoController.get()"]
    B --> C["ConsultarHistoricoService.executar(usuario_id)"]
    C --> D["SimuladoRepository.listar_historico_por_usuario()"]
    D --> E[("SELECT ... FROM simulados s<br/>JOIN resultados r JOIN categorias c<br/>WHERE s.usuario_id = :usuario_id<br/>ORDER BY s.data_realizacao DESC")]
    C --> F["SimuladoRepository.calcular_estatisticas()"]
    F --> G[("SELECT COUNT, AVG, MAX, MIN (r.nota)<br/>FROM resultados JOIN simulados")]
    E --> H["Service formata datas e monta<br/>{estatisticas, simulados}"]
    G --> H
    H --> I["Controller: JSON 200"]
    I --> J["Tela mostra média, melhor nota e a lista de simulados"]
```

---

## 3. Entrada de dados — Criar conta com aceite dos termos

Tela `index.html` (Crie sua conta) → `POST /auth/registro`

```mermaid
flowchart TD
    A["Tela: aluno preenche nome, e-mail, senha<br/>e marca 'Li e aceito os Termos'"] --> A1{"checkbox marcado?"}
    A1 -->|não| A2["Tela avisa: aceite os termos"]
    A1 -->|sim| B["fetch POST /auth/registro<br/>{nome, email, senha, aceitou_termos}"]
    B --> C["RegistroController.post()<br/>lê o JSON"]
    C --> D["RegistrarUsuarioService.executar()"]
    D --> E{"Validações: campos, e-mail,<br/>senha ≥ 4, termos aceitos"}
    E -->|falha| E1["ValueError → 400"] --> Z
    E -->|ok| F["UsuarioRepository.buscar_id_por_email()"]
    F --> G[("SELECT id FROM usuarios<br/>WHERE LOWER(email) = LOWER(:email)")]
    G --> H{"e-mail já existe?"}
    H -->|sim| E1
    H -->|não| I["Model Usuario: definir_senha() (hash)<br/>registrar_aceite_termos() (data/hora)"]
    I --> J["UsuarioRepository.contar_usuarios()<br/>SELECT COUNT(*) FROM usuarios"]
    J --> K["is_admin = (primeiro usuário?)"]
    K --> L["usuario.salvar() — CRUD da Model"]
    L --> M[("INSERT INTO usuarios (...)")]
    M --> N["Controller gera o token<br/>e devolve 201 {token, usuario}"]
    N --> Z["Tela guarda o token e abre o painel"]
```

## 4. Entrada de dados — Finalizar um simulado

Tela `painel.html` (Quiz) → `POST /simulados/<id>/finalizar`

```mermaid
flowchart TD
    A["Tela: aluno responde a última questão<br/>e clica em Finalizar Simulado"] -->|"POST /simulados/7/finalizar<br/>{respostas:[{item_id, alternativa_id}]}"| B["FinalizarSimuladoController.post(id)"]
    B --> C["FinalizarSimuladoService.executar()"]
    C --> D["Simulado.buscar_por_id(id)<br/>(CRUD da Model)"]
    D --> E{"existe? é do aluno?<br/>ainda não finalizado?"}
    E -->|não existe| E1["404"]
    E -->|outro aluno| E2["403 - Acesso negado"]
    E -->|já finalizado| E3["400"]
    E -->|ok| F["Valida: cada alternativa pertence<br/>à questão do item"]
    F --> G["ItemSimulado.corrigir()<br/>compara com Questao.alternativa_correta()"]
    G --> H["Simulado.calcular_pontuacao()"]
    H --> I["Resultado(nota).salvar()"]
    I --> J[("UPDATE itens_simulado ...<br/>INSERT INTO resultados ...")]
    J --> K["Controller: JSON 200 com a nota"]
    K --> L["Tela de resultado: nota, acertos,<br/>Aprovado / Continue estudando"]
```
