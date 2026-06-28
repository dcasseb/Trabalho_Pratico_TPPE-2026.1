# Curadoria de Dados de Autoria Científica – TP1 (TDD)

UnB · FCTE · TPPE – Técnicas de Programação para Plataformas Emergentes

---

## Integrantes do Grupo

| Nome             | Matrícula |
| ---------------- | --------- |
| Davi Casseb      | 211031682 |
| Nathan Abreu     | 221022696 |
| Douglas Marinho  | 221037465 |
| Igor Justino     | 211061897 |
| Henrique Alencar | 211061860 |

---

## Linguagem e Framework

- **Linguagem:** Python 3.x (orientada a objetos)
- **Framework de testes:** [pytest](https://docs.pytest.org/) – versão **9.0.3**
- **Cobertura:** [coverage.py](https://coverage.readthedocs.io/) – versão 7.14.1

---

## Casos Implementados

| Caso | Descrição |
|------|-----------|
| 1 | Diferenças de grafia tipográficas (acentuação, cedilha, apóstrofo) |
| 2 | Sobrenome + iniciais dos nomes (com ou sem pontos nas iniciais) |
| 3 | Partículas *de/da/do* opcionais e uso opcional de ponto em abreviações |
| 4 | Iniciais dos nomes agrupadas + sobrenome (ex.: "SH Guaraldi") |
| 5 | IDs diferentes para o mesmo autor – unificação pelo menor ID |

---

## Refatorações (Entrega 2)

| Classe/Método | Refatoração | Descrição |
| - | - | - |
| `Deduplicador::sao_equivalentes_tipografia()` | Extrair Método | A expressão que comparava as duas normalizações tipográficas foi extraída para o método `_normalizacoes_sao_iguais()`, separando a validação (intenção) da regra de comparação propriamente dita. |
| `Deduplicador::unificar_ids()` | Substituir Método por Objeto Método | O método `Deduplicador::unificar_ids()` era longo, com variáveis locais (`n`, `pai`, `grupos`, `min_id_por_grupo`) e funções aninhadas. Ele foi transformado no objeto `UnificadorIds`: cada variável local virou um atributo de instância e o corpo do método foi quebrado em métodos privados coesos, facilitando leitura e teste. |
| `Deduplicador` | Extrair classe | A estrutura Union-Find (conjuntos disjuntos) estava embutida em `Deduplicador::unificar_ids()` na forma da lista `pai` e das funções aninhadas `encontrar()` e `unir()`. Essa estrutura é uma responsabilidade coesa e independente do domínio de deduplicação, então foi extraída para a classe `ConjuntosDisjuntos`. |

---

## Como Executar os Testes

### Pré-requisitos

```bash
pip install -r requirements.txt
```

### Executar todos os testes

```bash
pytest
```

### Executar com relatório de cobertura

```bash
pytest --cov=src --cov-report=term-missing
```

### Executar um caso específico (por mark)

```bash
pytest -m caso1   # Caso 1 – Diferenças tipográficas
pytest -m caso2   # Caso 2 – Sobrenome + iniciais
pytest -m caso3   # Caso 3 – Partículas e pontos
pytest -m caso4   # Caso 4 – Iniciais agrupadas
pytest -m caso5   # Caso 5 – IDs diferentes
```

### Executar um arquivo de testes específico

```bash
pytest tests/test_caso1_grafia.py -v
```