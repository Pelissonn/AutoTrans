# Diagrama de classes do domínio

Classes implementadas em `backend/models/` e seus relacionamentos. O GitHub
renderiza o diagrama abaixo automaticamente (sintaxe Mermaid). O mesmo
diagrama está em [`diagrama_classes.mmd`](diagrama_classes.mmd).

```mermaid
classDiagram
    direction TB

    class ModeloBase {
        <<abstract>>
        +int id
        +salvar() ModeloBase
        +atualizar(campos) ModeloBase
        +deletar() void
        +listar_todos()$ list
        +buscar_por_id(id)$ ModeloBase
    }

    class Usuario {
        +str nome
        +str email
        +str senha_hash
        +str foto_url
        +bool is_admin
        +bool aceitou_termos
        +datetime data_aceite_termos
        +datetime data_criacao
        +datetime data_atualizacao
        +definir_senha(senha) void
        +verificar_senha(senha) bool
        +registrar_aceite_termos() void
        +to_dict() dict
    }

    class Categoria {
        +str nome
        +str descricao
        +to_dict() dict
    }

    class Material {
        +int categoria_id
        +str conteudo
        +str url
        +to_dict() dict
    }

    class Questao {
        +int categoria_id
        +str enunciado
        +alternativa_correta() Alternativa
        +to_dict() dict
    }

    class Alternativa {
        +int questao_id
        +str texto
        +bool correta
        +to_dict() dict
    }

    class Simulado {
        +int usuario_id
        +int categoria_id
        +str titulo
        +float pontuacao_max
        +datetime data_realizacao
        +calcular_pontuacao() float
        +pertence_a(usuario_id) bool
        +to_dict() dict
    }

    class ItemSimulado {
        +int simulado_id
        +int questao_id
        +int alternativa_escolhida_id
        +bool acerto
        +corrigir() bool
        +to_dict() dict
    }

    class Resultado {
        +int simulado_id
        +float nota
        +datetime data_resultado
        +aprovado(pontuacao_max) bool
        +to_dict() dict
    }

    class Favorito {
        +int usuario_id
        +int questao_id
        +datetime data_criacao
        +to_dict() dict
    }

    ModeloBase <|-- Usuario
    ModeloBase <|-- Categoria
    ModeloBase <|-- Material
    ModeloBase <|-- Questao
    ModeloBase <|-- Alternativa
    ModeloBase <|-- Simulado
    ModeloBase <|-- ItemSimulado
    ModeloBase <|-- Resultado
    ModeloBase <|-- Favorito

    Categoria "1" *-- "0..*" Questao : possui
    Categoria "1" *-- "0..*" Material : possui
    Questao "1" *-- "2..*" Alternativa : possui
    Usuario "1" *-- "0..*" Simulado : realiza
    Usuario "1" *-- "0..*" Favorito : marca
    Questao "1" *-- "0..*" Favorito : favoritada em
    Simulado "1" *-- "1..*" ItemSimulado : contém
    Simulado "1" *-- "0..1" Resultado : gera
    Simulado "0..*" o-- "1" Categoria : baseado em
    ItemSimulado "0..*" --> "1" Questao : refere-se a
    ItemSimulado "0..*" --> "0..1" Alternativa : escolhida
```

## Legenda

| Símbolo | Significado | Onde aparece |
|---|---|---|
| `<\|--` | **Herança** | Todas as Models herdam de `ModeloBase` (que herda de `db.Model`) e recebem o CRUD: `salvar()`, `atualizar()`, `deletar()`, `listar_todos()` e `buscar_por_id()`. |
| `*--` | **Composição** (a parte não existe sem o todo; é apagada em cascata) | Questões/materiais da categoria, alternativas da questão, simulados e favoritos do usuário, itens e resultado do simulado. |
| `o--` | **Agregação** (relação "usa", sem posse) | O simulado é baseado em uma categoria, mas não é dono dela — por isso a categoria não pode ser excluída se já tiver simulados. |
| `-->` | **Associação** | O item do simulado aponta para a questão e para a alternativa escolhida. |

## Correspondência com o banco

| Classe | Tabela | Arquivo |
|---|---|---|
| Usuario | `usuarios` | `backend/models/usuario.py` |
| Categoria | `categorias` | `backend/models/categoria.py` |
| Material | `materiais` | `backend/models/material.py` |
| Questao | `questoes` | `backend/models/questao.py` |
| Alternativa | `alternativas` | `backend/models/alternativa.py` |
| Simulado | `simulados` | `backend/models/simulado.py` |
| ItemSimulado | `itens_simulado` | `backend/models/item_simulado.py` |
| Resultado | `resultados` | `backend/models/resultado.py` |
| Favorito | `favoritos` | `backend/models/favorito.py` |
