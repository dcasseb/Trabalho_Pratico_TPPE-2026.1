import pytest
from src.deduplicador import Deduplicador


@pytest.mark.caso4
class TestIniciaisAgrupadas:
    """
    Suite – Caso 4: Iniciais dos nomes agrupadas + sobrenome.

    Verifica que nomes em que os primeiros nomes são representados por
    iniciais agrupadas (ex.: "VC Junior", "SH Guaraldi") são reconhecidos
    como equivalentes ao nome completo correspondente.
    """

    @pytest.fixture(autouse=True)
    def _setup(self, deduplicador):
        self.ded = deduplicador

# Testes parametrizados – pares equivalentes (dataset 1 e 2)

    @pytest.mark.parametrize(
        "nome_completo, nome_abreviado",
        [
            # Dataset 1 – dados do enunciado
            ("Vanilda Cristina Junior", "VC Junior"),
            ("Sérgio Henrique Guaraldi", "SH Guaraldi"),
            # Dataset 2 – variações adicionais
            ("Monica Hirata Sant'anna", "MH Sant'anna"),
            ("Raphael Goncalves Viana", "RG Viana"),
            ("Lilian Luiza Viana Vieira", "LLV Vieira"),
        ],
    )
    def test_iniciais_agrupadas_equivalente(self, nome_completo: str, nome_abreviado: str):
        # existe: indexadores usam "SH Guaraldi" em vez do nome completo; devem ser unificados
        assert self.ded.sao_equivalentes_iniciais_agrupadas(nome_completo, nome_abreviado) is True

# Testes parametrizados – pares NÃO equivalentes

    @pytest.mark.parametrize(
        "nome_completo, nome_abreviado",
        [
            # Iniciais erradas
            ("Vanilda Cristina Junior", "VX Junior"),
            ("Sérgio Henrique Guaraldi", "SG Guaraldi"),
            # Sobrenome diferente
            ("Vanilda Cristina Junior", "VC Santos"),
            # Abreviado não possui iniciais agrupadas
            ("Vanilda Cristina Junior", "Vanilda C. Junior"),
        ],
    )
    def test_iniciais_agrupadas_nao_equivalente(self, nome_completo: str, nome_abreviado: str):
        # existe: iniciais ou sobrenome errados não devem gerar falso-positivo
        assert self.ded.sao_equivalentes_iniciais_agrupadas(nome_completo, nome_abreviado) is False

    # ------------------------------------------------------------------
    # Testes de exceção
    # ------------------------------------------------------------------

    def test_excecao_nome_completo_none(self):
        # TypeError: None não pode ser decomposto em lista de partes
        with pytest.raises(TypeError):
            self.ded.sao_equivalentes_iniciais_agrupadas(None, "VC Junior")

    def test_excecao_nome_abreviado_none(self):
        # TypeError: abreviado None impede detecção de iniciais agrupadas
        with pytest.raises(TypeError):
            self.ded.sao_equivalentes_iniciais_agrupadas("Vanilda Cristina Junior", None)

    def test_excecao_nome_completo_vazio(self):
        # ValueError: nome vazio não tem partes para extrair iniciais
        with pytest.raises(ValueError):
            self.ded.sao_equivalentes_iniciais_agrupadas("", "VC Junior")

    def test_excecao_nome_abreviado_vazio(self):
        # ValueError: abreviado vazio não contém bloco de iniciais agrupadas
        with pytest.raises(ValueError):
            self.ded.sao_equivalentes_iniciais_agrupadas("Vanilda Cristina Junior", "")
