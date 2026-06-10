import pytest
from src.deduplicador import Deduplicador


@pytest.mark.caso1
class TestDiferencasGrafia:

    @pytest.fixture(autouse=True)
    def _setup(self, deduplicador):
        self.ded = deduplicador

    @pytest.mark.parametrize(
        "nome1, nome2",
        [
            ("Monica Hirata Sant`anna", "Mônica Hirata Sant'anna"),
            ("Sergio Henrique Guaraldi", "Sérgio Henrique Guaraldi"),
            ("Veronica de Oliveira Moreira", "Verônica de Oliveira Moreira"),
            ("Lilian Luiza Viana Vieira", "Lílian Luíza Viana Vieira"),
            ("Monica Hirata Sant'anna", "Mônica Hirata Sant’anna"),
            ("Cassius de Souza", "Cassius de Souza"),
            ("Raphael Goncalves Viana", "Raphael Gonçalves Viana"),
            ("Vanilda Cristina Junior", "Vanilda Cristina Júnior"),
        ],
    )
    def test_nomes_equivalentes_tipografia(self, nome1, nome2):
        assert self.ded.sao_equivalentes_tipografia(nome1, nome2) is True

    @pytest.mark.parametrize(
        "nome1, nome2",
        [
            ("Ana de Mattos Seabra", "Ana de Oliveira Seabra"),
            ("Monica Hirata Santanna", "Joana Hirata Sant'anna"),
            ("Carlos Silva", "Carlos Santos"),
            ("Sérgio Guaraldi", "Sérgio Henrique Guaraldi"),
        ],
    )
    def test_nomes_nao_equivalentes_tipografia(self, nome1, nome2):
        assert self.ded.sao_equivalentes_tipografia(nome1, nome2) is False

    def test_excecao_nome1_none(self):
        with pytest.raises(TypeError):
            self.ded.sao_equivalentes_tipografia(None, "Ana de Mattos Seabra")

    def test_excecao_nome2_none(self):
        with pytest.raises(TypeError):
            self.ded.sao_equivalentes_tipografia("Ana de Mattos Seabra", None)

    def test_excecao_nome1_vazio(self):
        with pytest.raises(ValueError):
            self.ded.sao_equivalentes_tipografia("", "Ana de Mattos Seabra")

    def test_excecao_nome2_apenas_espacos(self):
        with pytest.raises(ValueError):
            self.ded.sao_equivalentes_tipografia("Ana de Mattos Seabra", "   ")
