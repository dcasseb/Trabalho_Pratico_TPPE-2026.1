import pytest
from src.deduplicador import Deduplicador


@pytest.fixture
def ded(deduplicador):
    return deduplicador


class TestValidarNomesTipoInvalido:

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


class TestAbreviacaoNomeCompletoUmaParte:

    def test_nome_completo_apenas_um_token(self, ded):
        resultado = ded.sao_equivalentes_abreviacao("de Seabra", "A. Seabra")
        assert resultado is False

    def test_nome_completo_particula_unica(self, ded):
        resultado = ded.sao_equivalentes_abreviacao("Seabra", "S. Seabra")
        assert resultado is False


class TestParticulasBranchAssimetrico:

    def test_p2_inicial_p1_comeca_com_p2(self, ded):
        resultado = ded.sao_equivalentes_particulas("Seabra", "S.")
        assert resultado is True

    def test_combinacao_inicial_inversa(self, ded):
        resultado = ded.sao_equivalentes_particulas("S.", "Seabra")
        assert resultado is True


class TestIniciaisAgrupadasNomeCompletoUmaParte:

    def test_nome_completo_so_sobrenome(self, ded):
        resultado = ded.sao_equivalentes_iniciais_agrupadas("Guaraldi", "SH Guaraldi")
        assert resultado is False

    def test_nome_completo_particula_mais_sobrenome(self, ded):
        resultado = ded.sao_equivalentes_iniciais_agrupadas("de Guaraldi", "SH Guaraldi")
        assert resultado is False


class TestSaoMesmoAutorCaptura:

    def test_registros_com_nome_vazio_nao_levanta(self, ded):
        registros = [(1, "Ana Seabra"), (2, "")]
        resultado = ded.unificar_ids(registros)
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
