"""
Testes de cobertura extra — cobrem os ramos não alcançados pelos testes principais.

Ramos cobertos aqui:
  - _validar_nomes com valor não-str e não-None (int, list, etc.)
  - Caso 2: nome_completo com < 2 partes após remover partículas
  - Caso 3: branch assimétrico len(p2)==1 e p1 começa com p2
  - Caso 4: nome_completo com < 2 partes após remover partículas
  - _sao_mesmo_autor: captura de TypeError/ValueError interno
"""
import pytest
from src.deduplicador import Deduplicador


@pytest.fixture
def ded(deduplicador):
    return deduplicador

# _validar_nomes — argumento não-str e não-None

class TestValidarNomesTipoInvalido:
    # existe: _validar_nomes deve rejeitar int, list, dict, float com TypeError

    def test_caso1_nome1_inteiro(self, ded):
        with pytest.raises(TypeError):
            ded.sao_equivalentes_tipografia(123, "Ana Seabra")

    def test_caso1_nome2_lista(self, ded):
        with pytest.raises(TypeError):
            ded.sao_equivalentes_tipografia("Ana Seabra", ["Ana"])

    def test_caso2_nome_completo_dict(self, ded):
        with pytest.raises(TypeError):
            ded.sao_equivalentes_abreviacao({"nome": "Ana"}, "A. Seabra")

    def test_caso3_nome1_float(self, ded):
        with pytest.raises(TypeError):
            ded.sao_equivalentes_particulas(3.14, "Ana Seabra")

    def test_caso4_nome_abreviado_inteiro(self, ded):
        with pytest.raises(TypeError):
            ded.sao_equivalentes_iniciais_agrupadas("Ana Seabra", 42)

# Caso 2 — nome_completo com apenas 1 parte após remover partículas

class TestAbreviacaoNomeCompletoUmaParte:
    # existe: nome com < 2 tokens reais após remover partículas não pode ter inicial — deve retornar False

    def test_nome_completo_apenas_um_token(self, ded):
        # "de" é partícula; após remover sobra só "Seabra" → < 2 partes → False
        resultado = ded.sao_equivalentes_abreviacao("de Seabra", "A. Seabra")
        assert resultado is False

    def test_nome_completo_particula_unica(self, ded):
        # Só um nome real (sem partículas) não pode ter iniciais
        resultado = ded.sao_equivalentes_abreviacao("Seabra", "S. Seabra")
        assert resultado is False

# Caso 3 — branch assimétrico: p2 é inicial, p1 começa com p2

class TestParticulasBranchAssimetrico:
    # existe: cobre o branch em que p2 é a inicial e p1 é o nome completo (direção inversa)

    def test_p2_inicial_p1_comeca_com_p2(self, ded):
        # Sem partículas; p1="seabra" (completo), p2="s" (inicial de Seabra)
        # Deve entrar no branch: len(p2)==1 and p1.startswith(p2) → True
        resultado = ded.sao_equivalentes_particulas("Seabra", "S.")
        assert resultado is True

    def test_combinacao_inicial_inversa(self, ded):
        # p1 é a inicial, p2 é o nome completo (branch len(p1)==1)
        resultado = ded.sao_equivalentes_particulas("S.", "Seabra")
        assert resultado is True


# Caso 4 — nome_completo com < 2 partes após filtro de partículas

class TestIniciaisAgrupadasNomeCompletoUmaParte:
    # existe: nome completo com 1 token real após filtro não tem primeiros nomes para extrair iniciais

    def test_nome_completo_so_sobrenome(self, ded):
        # "Guaraldi" sozinho: após filtro só 1 parte → False
        resultado = ded.sao_equivalentes_iniciais_agrupadas("Guaraldi", "SH Guaraldi")
        assert resultado is False

    def test_nome_completo_particula_mais_sobrenome(self, ded):
        # "de Guaraldi": "de" removido → 1 parte → False
        resultado = ded.sao_equivalentes_iniciais_agrupadas("de Guaraldi", "SH Guaraldi")
        assert resultado is False

# _sao_mesmo_autor — captura interna de TypeError/ValueError

class TestSaoMesmoAutorCaptura:
    # existe: _sao_mesmo_autor captura TypeError/ValueError internos; deve retornar False sem propagar

    def test_registros_com_nome_vazio_nao_levanta(self, ded):
        # Nome vazio dentro da lista causa ValueError internamente; deve retornar False
        registros = [(1, "Ana Seabra"), (2, "")]
        resultado = ded.unificar_ids(registros)
        # IDs devem permanecer distintos (não são o mesmo autor)
        ids = [r[0] for r in resultado]
        assert 1 in ids and 2 in ids

    def test_tres_variantes_mesmo_autor_menor_id(self, ded):
        registros = [
            (500, "Sergio Henrique Guaraldi"),
            (100, "Sérgio Henrique Guaraldi"),
            (300, "SH Guaraldi"),
        ]
        resultado = ded.unificar_ids(registros)
        ids = [r[0] for r in resultado]
        assert all(id_ == 100 for id_ in ids)

    def test_registros_sem_duplicatas_mantidos(self, ded):
        registros = [(10, "Carlos Silva"), (20, "Pedro Santos")]
        resultado = ded.unificar_ids(registros)
        assert resultado[0][0] == 10
        assert resultado[1][0] == 20
