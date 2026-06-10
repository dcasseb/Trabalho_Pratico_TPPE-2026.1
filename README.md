# Curadoria de Dados de Autoria Científica – TP1 (TDD)

UnB · FCTE · TPPE – Técnicas de Programação para Plataformas Emergentes

---

## Integrantes do Grupo

| Nome | Matrícula |
| Davi Casseb | 211031682 |
| Nathan Abreu |  221022696 |
| Douglas Marinho | 221037465 |
| Igor Justino | 211061897 |
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

README a ser concluído
