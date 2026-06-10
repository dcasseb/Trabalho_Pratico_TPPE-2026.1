import pytest
from src.deduplicador import Deduplicador


@pytest.mark.caso4
class TestIniciaisAgrupadas:

    @pytest.fixture(autouse=True)
    def _setup(self, deduplicador):
        self.ded = deduplicador

    @pytest.mark.parametrize(
        "nome_completo, nome_abreviado",
        [
            ("Vanilda Cristina Junior", "VC Junior"),
            ("Sérgio Henrique Guaraldi", "SH Guaraldi"),
            ("Monica Hirata Sant'anna", "MH Sant'anna"),
            ("Raphael Goncalves Viana", "RG Viana"),
            ("Lilian Luiza Viana Vieira", "LLV Vieira"),
        ],
    )
    def test_iniciais_agrupadas_equivalente(self, nome_completo, nome_abreviado):
        assert self.ded.sao_equivalentes_iniciais_agrupadas(nome_completo, nome_abreviado) is True

    @pytest.mark.parametrize(
        "nome_completo, nome_abreviado",
        [
            ("Vanilda Cristina Junior", "VX Junior"),
            ("Sérgio Henrique Guaraldi", "SG Guaraldi"),
            ("Vanilda Cristina Junior", "VC Santos"),
            ("Vanilda Cristina Junior", "Vanilda C. Junior"),
        ],
    )
    def test_iniciais_agrupadas_nao_equivalente(self, nome_completo, nome_abreviado):
        assert self.ded.sao_equivalentes_iniciais_agrupadas(nome_completo, nome_abreviado) is False

    def test_excecao_nome_completo_none(self):
        with pytest.raises(TypeError):
            self.ded.sao_equivalentes_iniciais_agrupadas(None, "VC Junior")

    def test_excecao_nome_abreviado_none(self):
        with pytest.raises(TypeError):
            self.ded.sao_equivalentes_iniciais_agrupadas("Vanilda Cristina Junior", None)

    def test_excecao_nome_completo_vazio(self):
        with pytest.raises(ValueError):
            self.ded.sao_equivalentes_iniciais_agrupadas("", "VC Junior")

    def test_excecao_nome_abreviado_vazio(self):
        with pytest.raises(ValueError):
            self.ded.sao_equivalentes_iniciais_agrupadas("Vanilda Cristina Junior", "")
